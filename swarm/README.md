# Research swarm (Claude Managed Agents)

A lead agent with three specialists, run on demand. Each run is one session with a hard spend cap.

| Agent | Model | Role |
|---|---|---|
| Swarm Orchestrator | `claude-opus-5-5` | Decomposes, dispatches, adjudicates, writes the brief |
| Scout | `claude-haiku-5-5` | One inquiry vector per spawn; web and uploaded files; writes evidence JSON |
| Analyst | `claude-sonnet-5-5` | Correlations, knowledge graph, ranked hypotheses, gaps; the only agent with a shell |
| Red-Team | `claude-sonnet-5-5` | Tries to disprove each hypothesis; independent parallel passes |

## One-time setup

Needs the `ant` CLI 1.40.0 or later and `pip install -r swarm/requirements.txt`. Run from the repo root.

```bash
ant auth login
```

```bash
ant apply --dry-run -v swarm/agents/orchestrator.md swarm/environments/swarm.yaml swarm/environments/swarm-locked.yaml
```

```bash
ant apply swarm/agents/orchestrator.md swarm/environments/swarm.yaml swarm/environments/swarm-locked.yaml
```

The orchestrator file references the other three agents, so they are created with it. Commit the
`claude-lock.json` this writes: it holds the IDs, and without it the next apply creates duplicates.
After editing any agent file, run the same `ant apply` again.

## Run

```bash
python swarm/run.py "Your problem statement" --upload path/to/file.xlsx --budget 15
```

- `--upload` is repeatable. Files are mounted read-only at `/mnt/session/uploads/`.
- `--budget` is a hard cap in USD at list prices (default 15, or `SWARM_BUDGET_USD`). At the cap the
  session pauses and keeps its work; the script asks for a new cap, or resume later with
  `python swarm/run.py --resume <session id> --budget <new total>`.
- `--max-iterations` sets how many times the grader can send the brief back (default 3).
- Deliverables are saved to `swarm/runs/<session id>/`.

## Sandbox security

Two environments, chosen per run:

- **Default (open web).** Researching arbitrary sources needs unrestricted networking, which also opens
  egress from the sandbox. To keep that egress out of reach, every agent that reads the web
  (Orchestrator, Scout, Red-Team) has no shell, and the only agent with a shell (Analyst) has no web
  tools and is told to make no network requests. Residual risk: text planted in a web page could reach
  the Analyst through an evidence file. Shell calls are also screened by the `auto` permission policy.
- **`--offline` (locked).** No sandbox egress and no web results; the swarm works from uploads only.
  Use this for confidential files. To allow named sources, add `allowed_hosts` in
  `swarm/environments/swarm-locked.yaml` and re-apply.

## Tuning cost

- Workflow runs (large fan-outs of Scouts) are on. To turn them off, set `workflows: {type: disabled}`
  in `swarm/agents/orchestrator.md` and re-apply.
- For more rigor at higher cost, change Analyst and Red-Team to `claude-opus-5-5`.
- The rubric the grader scores against is `RUBRIC` in `swarm/run.py`.
