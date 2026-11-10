---
name: research-swarm
description: Run the multi-agent research swarm (Scout, Analyst, Red-Team, Orchestrator on Claude Managed Agents) on an ambiguous or multi-domain problem and return a decision brief. Use only when the user explicitly asks for the swarm or invokes /research-swarm; it spends money per run.
---

# Research swarm

Runs one Managed Agents session via `swarm/run.py`. Trigger only on explicit request.

1. Get the problem statement from the user's message. Ask which local files to include, if any, and the spend cap if they did not give one (default 15 USD).
2. Confirm the cap with the user before starting: each run spends real money.
3. From the repo root, run in the background (runs take minutes to hours):

   `python swarm/run.py "<problem>" --upload <file> --budget <usd>`

   If the uploads are confidential, add `--offline` (no web, no sandbox egress) and say so to the user.
   Write a long problem to a file and pass `@path` instead.
4. If it stops with `budget_reached`, tell the user what was spent and ask whether to resume with `python swarm/run.py --resume <session id> --budget <new total>`.
5. When it finishes, read `swarm/runs/<session id>/brief.md` and give the user the bottom line, the surviving hypotheses, and the path to the full brief.

If it reports no ID for the agent or environment, setup has not been done: point the user to `swarm/README.md`.
