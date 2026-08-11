# OpenGrants OS

**The open-source Autonomous Agentic AI MCP Server for grants, public-goods funding, and open-source AI sustainability.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-Server-purple.svg)](https://modelcontextprotocol.io)
[![Version](https://img.shields.io/badge/Version-0.2.0-green.svg)]()
[![GitHub](https://img.shields.io/badge/GitHub-ANAMIZED%2Fopengrants--os-black.svg)](https://github.com/ANAMIZED/opengrants-os)

> Eliminate the discovery tax. Treat traditional grants **and** donations / sponsorships / quadratic funding as equal first-class citizens so open-source AI and public-goods projects can compete on a level playing field.

## Why OpenGrants OS?

Most funding tools are either closed SaaS or fragmented portals. OpenGrants OS is:

- A **first-class MCP Server** any agent (Claude, Cursor, custom agents) can call
- An **autonomous multi-agent system** (LangGraph) for discovery → ranking → drafting → evaluation
- Explicitly optimized for **open-source AI**, open weights, and **public-goods funding**
- Fully open-source (Apache 2.0), self-hostable, and provenance-first
- Already dogfooding itself (see `docs/DOGFOODING_OPENGRANTS.md`)

## Features (v0.2.0)

| Capability | Status |
|------------|--------|
| Live Grants.gov search | ✅ |
| NSF Awards search | ✅ |
| Public-goods / donation sources (GitHub Sponsors, Open Collective, Gitcoin, OpenSSF, NumFOCUS, PSF, NLnet, Prototype Fund…) | ✅ |
| Profile Steward | ✅ |
| Grounded proposal drafting (grants + sponsorship vehicles) | ✅ |
| Continuous ingestion + evaluation harness | ✅ |
| Multi-agent ranking with open-source bias | ✅ |
| FUNDING.yml ready | ✅ |

## Quick Start

```bash
git clone https://github.com/ANAMIZED/opengrants-os.git
cd opengrants-os
pip install -e .
python -m opengrants          # starts the MCP server (stdio)
```

### One-line MCP client config (Claude Desktop / Cursor)

```json
{
  "mcpServers": {
    "opengrants": {
      "command": "python",
      "args": ["-m", "opengrants"],
      "cwd": "/absolute/path/to/opengrants-os"
    }
  }
}
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `search_grants` | Live Grants.gov keyword search with full provenance |
| `get_grant_details` | Detail view for a specific opportunity |
| `list_open_source_relevant_grants` | Open-source / AI biased discovery |
| `list_public_goods_funding` | **Donations, sponsorships, quadratic & open-source funds** |
| `search_nsf_awards` | NSF Awards public API |
| `refresh_corpus` | Continuous ingestion into local corpus |
| `run_evaluation` | Discovery + open-source relevance harness |
| `upsert_profile` | Create / update project or researcher profile |
| `draft_proposal_outline` | Grounded outline + short pitch (works for grants **and** public-goods vehicles) |

## Resources

- `opengrants://status`
- `opengrants://sources`

## Support the Project

OpenGrants is public-goods infrastructure. You can support it via:

- GitHub Sponsors (enable on the account → Sponsor button appears)
- Open Collective (create a collective and update `.github/FUNDING.yml`)
- See `docs/DOGFOODING_OPENGRANTS.md` for the full self-generated proposal outline

## Architecture

```
MCP Interface
    ↓
Discovery (Grants.gov · NSF · Public-Goods Catalog)
    ↓
Profile Steward → Ranking Agents → Drafting Agents
    ↓
Evaluation & Continuous Corpus
```

## Development

```bash
pip install -e ".[dev,agents]"
ruff check .
python -m opengrants.evaluation.harness
```

## Publishing & Discovery

- Official MCP Registry: `server.json` present → `mcp-publisher publish`
- Glama: `glama.json` present
- PyPI: ready (`hatch build && twine upload dist/*`)
- GitHub topics (recommended): `mcp`, `model-context-protocol`, `grants`, `open-source`, `ai`, `agentic`, `public-goods`, `funding`, `langgraph`, `open-weight`

## License

Apache License 2.0 — see [LICENSE](LICENSE).

---

**Built for the open-source AI community.**  
Make the funding landscape as open as the code we write.

https://github.com/ANAMIZED/opengrants-os
