#!/usr/bin/env python3
"""Trigger one research-swarm session on Claude Managed Agents.

    python swarm/run.py "Why is X happening and what should we do?" \
        --upload models/deck.xlsx --upload notes.pdf --budget 15

Setup happens once with `ant apply` (see swarm/README.md); this script only
starts sessions against the stored agent and environment IDs.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parent
LOCK_CANDIDATES = [Path.cwd() / "claude-lock.json", ROOT.parent / "claude-lock.json", ROOT / "claude-lock.json"]

# Starter rubric - tune the criteria to your own quality bar.
RUBRIC = """# Research brief rubric (starter - tune the criteria)
- The brief exists at /mnt/session/outputs/brief.md and opens with a bottom-line answer of at most five lines that states a confidence level
- Every factual claim cites a source URL or a file path
- At least three distinct hypotheses are stated, each with supporting evidence
- Each hypothesis carries a Red-Team verdict (survives, weakened or refuted) and its strongest counter-argument
- Contradictions between sources are listed, and each is resolved or explicitly marked open
- A decision matrix compares the options on evidence strength, risk and reversibility
- A recommended plan lists concrete next actions in order
- Known gaps are listed along with the data that would close each one
- Any code, model or data file the brief references exists in /mnt/session/outputs/
- No placeholder text, TODOs or empty sections remain
"""


def lock_id(suffix: str, env_var: str) -> str:
    """Resource ID from an env var, else from claude-lock.json written by `ant apply`."""
    if os.getenv(env_var):
        return os.environ[env_var]
    for lock in LOCK_CANDIDATES:
        if lock.exists():
            resources = json.loads(lock.read_text()).get("resources", {})
            for path, entry in resources.items():
                if path.replace("\\", "/").endswith(suffix):
                    return entry["id"]
    sys.exit(f"No ID for {suffix}. Run `ant apply` (see swarm/README.md) or set {env_var}.")


def cents(dollars: float) -> str:
    return str(max(1, round(dollars * 100)))


def budget_param(dollars: float) -> dict:
    return {"type": "limit", "max_list_cost": {"amount": cents(dollars), "currency": "USD"}}


def spent_dollars(client: anthropic.Anthropic, session_id: str) -> float:
    usage = client.beta.sessions.retrieve(session_id).usage
    if usage is None or usage.list_cost is None:
        return 0.0
    return int(usage.list_cost.amount) / 100  # minor units (cents), like the budget


def raise_budget_interactively(client: anthropic.Anthropic, session_id: str) -> bool:
    """At the cap the session is paused, not dead. Only a budget change resumes it."""
    spent = spent_dollars(client, session_id)
    print(f"\n[budget] Cap reached at ${spent:.2f}. The session is paused and keeps its work.")
    if not sys.stdin.isatty():
        print(f"[budget] Resume later with: python swarm/run.py --resume {session_id} --budget <new total>")
        return False
    answer = input("[budget] New total cap in USD (blank to stop here): ").strip()
    if not answer:
        return False
    new_cap = float(answer)
    if new_cap <= spent:
        print("[budget] New cap must be above what is already spent. Stopping.")
        return False
    client.beta.sessions.update(session_id, budget=budget_param(new_cap))
    print(f"[budget] Raised to ${new_cap:.2f}. Resuming.")
    return True


def drain(client: anthropic.Anthropic, session_id: str, stream, kickoff: dict | None) -> str:
    """Follow the session until the work is done. Returns the final stop reason."""
    open_runs: set[str] = set()
    if kickoff:
        client.beta.sessions.events.send(session_id=session_id, events=[kickoff])
    for event in stream:
        match event.type:
            case "agent.message":
                for block in event.content:
                    if block.type == "text":
                        print(block.text, flush=True)
            case "agent.thread_message_sent":
                print(f"  -> {event.to_agent_name}", flush=True)
            case "agent.thread_message_received":
                print(f"  <- {event.from_agent_name} reported", flush=True)
            case "workflow_run.created":
                open_runs.add(event.workflow_run_id)
                print(f"  [run] {event.name} started", flush=True)
            case "workflow_run.status_ended":
                open_runs.discard(event.workflow_run_id)
                print(f"  [run] ended: {event.result.type}", flush=True)
            case "span.outcome_evaluation_end":
                print(f"\n[grader] iteration {event.iteration}: {event.result}\n{event.explanation}\n", flush=True)
            case "agent.tool_use" | "agent.mcp_tool_use":
                if event.evaluated_permission == "ask":
                    # Unattended: a paused call would wait forever, so deny it and tell the agent why.
                    client.beta.sessions.events.send(
                        session_id=session_id,
                        events=[{
                            "type": "user.tool_confirmation",
                            "tool_use_id": event.id,
                            "result": "deny",
                            "deny_message": "No human is available to approve this call. Find another way.",
                        }],
                    )
            case "session.status_idle":
                reason = event.stop_reason.type
                if reason == "requires_action":
                    continue
                if reason == "budget_reached":
                    if raise_budget_interactively(client, session_id):
                        continue
                    return reason
                if reason == "end_turn" and open_runs:
                    continue  # a workflow run is still open; the agent takes another turn when it ends
                return reason
            case "session.status_terminated":
                return "terminated"
    return "stream_closed"


def download_outputs(client: anthropic.Anthropic, session_id: str, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    files = []
    for _ in range(5):  # outputs are indexed a few seconds after the session goes idle
        files = list(client.beta.files.list(scope_id=session_id, betas=["managed-agents-2026-04-01"]).data)
        if files:
            break
        time.sleep(2)
    if not files:
        print("[outputs] none found.")
        return
    for f in files:
        target = out_dir / Path(f.filename).name
        client.beta.files.download(f.id).write_to_file(target)
        print(f"[outputs] {target}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the research swarm on one problem.")
    parser.add_argument("problem", nargs="?", help="Problem statement, or @path to a text file containing it")
    parser.add_argument("--upload", action="append", default=[], metavar="FILE", help="File for the swarm to read (repeatable)")
    parser.add_argument("--budget", type=float, default=float(os.getenv("SWARM_BUDGET_USD", "15")),
                        help="Hard spend cap in USD at list prices (default 15, or $SWARM_BUDGET_USD)")
    parser.add_argument("--max-iterations", type=int, default=3, help="Grader revision rounds (1-20, default 3)")
    parser.add_argument("--out", type=Path, default=None, help="Where to save deliverables (default swarm/runs/<session id>)")
    parser.add_argument("--offline", action="store_true",
                        help="Locked sandbox: no network egress and no web results; uploads only. Use for confidential files")
    parser.add_argument("--resume", metavar="SESSION_ID", help="Raise the cap on a budget-paused session to --budget and keep following it")
    args = parser.parse_args()

    client = anthropic.Anthropic()

    if args.resume:
        session_id = args.resume
        with client.beta.sessions.events.stream(session_id=session_id) as stream:
            client.beta.sessions.update(session_id, budget=budget_param(args.budget))
            print(f"[budget] Cap set to ${args.budget:.2f}. Resuming {session_id}.")
            reason = drain(client, session_id, stream, kickoff=None)
    else:
        if not args.problem:
            parser.error("problem is required unless --resume is given")
        problem = Path(args.problem[1:]).read_text() if args.problem.startswith("@") else args.problem
        if args.offline and not args.upload:
            parser.error("--offline has no web access, so it needs at least one --upload")
        if args.offline:
            problem += "\n\nThis run is offline: web search and fetch return nothing. Work only from the uploaded files."

        resources = []
        for path in map(Path, args.upload):
            with path.open("rb") as fh:
                uploaded = client.beta.files.upload(file=fh)
            # Lands read-only at /mnt/session/uploads/<name>
            resources.append({"type": "file", "file_id": uploaded.id, "mount_path": f"/{path.name}"})
            print(f"[upload] {path.name}")

        session = client.beta.sessions.create(
            agent=lock_id("swarm/agents/orchestrator.md", "SWARM_AGENT_ID"),
            environment_id=(
                lock_id("swarm/environments/swarm-locked.yaml", "SWARM_LOCKED_ENV_ID")
                if args.offline
                else lock_id("swarm/environments/swarm.yaml", "SWARM_ENV_ID")
            ),
            title=problem[:80],
            resources=resources,
            budget=budget_param(args.budget),  # create-only: it can be changed later but never added
        )
        session_id = session.id
        print(f"[session] {session_id}  cap ${args.budget:.2f}  network {'locked' if args.offline else 'open web'}")
        print(f"[watch]   https://platform.claude.com/workspaces/default/sessions/{session_id}\n")

        kickoff = {
            "type": "user.define_outcome",
            "description": (
                "Investigate the problem below with the swarm and write the decision brief to "
                "/mnt/session/outputs/brief.md.\n\n" + problem
            ),
            "rubric": {"type": "text", "content": RUBRIC},
            "max_iterations": args.max_iterations,
        }
        # Open the stream before sending the kickoff so no event is missed.
        with client.beta.sessions.events.stream(session_id=session_id) as stream:
            reason = drain(client, session_id, stream, kickoff)

    print(f"\n[done] {reason}. Spent ${spent_dollars(client, session_id):.2f} at list prices.")
    if reason == "retries_exhausted":
        print("[done] The agent gave up on an error. Open the session in the Console for details.")
    download_outputs(client, session_id, args.out or ROOT / "runs" / session_id)


if __name__ == "__main__":
    main()
