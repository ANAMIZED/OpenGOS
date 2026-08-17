---
name: multi-agent-workflow
description: OpenGOS multi-agent pipeline — discover → rank → draft under provenance.
---

# Multi-agent workflow (OpenGOS)

## Agents
- **discoverer** — Grants.gov / NSF / public-goods search
- **ranker** — open-source biased ranking
- **drafter** — grounded proposal outline

## Entry points
- MCP tools on `opengos`
- API: `POST /v1/workflows`
- Python: `opengos.agents.orchestrator`
