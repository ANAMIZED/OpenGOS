# AGENTS.md

Guidance for AI coding agents working on **OpenGOS**.

## What this project is

OpenGOS is an **autonomous agentic MCP server** for:

- Grant discovery (Grants.gov, NSF)
- Public-goods funding (sponsors, collectives, quadratic, open-source funds)
- Profile stewardship
- Grounded proposal drafting
- Ranking with a **declared open-source bias**

It treats traditional grants **and** donations/sponsorships as first-class funding paths so open-source projects can compete fairly.

## Repository layout

```
src/opengrants/
  server.py          # MCP entry point (FastMCP) — primary interface
  grants_client.py   # Grants.gov client + normalization
  agents/            # Orchestration agents
  drafting/          # Proposal outline / drafting
  evaluation/        # Evaluation harness
  ingestion/         # Corpus refresh
  profile/           # Project profile steward
  sources/           # NSF + public-goods catalog
  i18n.py            # Multilingual helpers

opengos.html         # Interactive browser shell (no install)
mcp-related:         # server.json, glama.json
docs/                # Human docs
```

## Conventions

- Python **3.11+**
- Package name on PyPI: `opengos`
- Import path: `opengrants`
- Entry point: `opengos` → `opengrants.server:main`
- MCP framework: **FastMCP**
- Lint/format: `ruff`
- Always preserve **provenance** (source + retrieved_at + official URL)
- Prefer grounded claims over speculation for any funding advice

## How to run

```bash
pip install -e ".[dev]"
opengos                    # starts MCP server on stdio
python -m opengrants       # same
```

## Boundaries (do not)

- Do not remove provenance fields from grant results
- Do not hardcode API keys (none are required for public sources)
- Do not treat public-goods funding as second-class vs federal grants
- Do not invent eligibility or award amounts — ground in source data
- Keep the MCP tool surface clear and stable

## Adding a new data source

1. Create an adapter under `src/opengrants/sources/`
2. Normalize into the shared opportunity / funding shape where possible
3. Wire it into `server.py` as a new `@mcp.tool`
4. Document it in README + `opengos://sources` resource

## Related files for agents

- `SKILL.md` — skill description for agent skill discovery
- `server.json` — MCP registry metadata
- `glama.json` — Glama registry metadata
