# OpenGOS

**Open-source Autonomous Agentic AI MCP Server for grants, public-goods funding, and open-source sustainability.**

Formerly referred to in early drafts as “OpenGrants OS.” Product name is now **OpenGOS** to avoid confusion with the commercial OpenGrants (opengrants.io) brand.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-Server-purple.svg)](https://modelcontextprotocol.io)
[![Version](https://img.shields.io/badge/Version-0.2.1-green.svg)]()
[![GitHub](https://img.shields.io/badge/GitHub-ANAMIZED%2Fopengrants--os-black.svg)](https://github.com/ANAMIZED/opengrants-os)

> Eliminate the discovery tax. Treat traditional grants **and** donations / sponsorships / quadratic funding as equal first-class citizens so open-source projects can compete on a level playing field.

## Try it now

**[Launch the interactive shell →](https://htmlpreview.github.io/?https://github.com/ANAMIZED/opengrants-os/blob/main/opengrants-os-1.html)**

A complete demo: Discover, Constellation (3D knowledge graph), Pipeline, Draft, Console, and Profile — one HTML file. No install required.

Source: [`opengrants-os-1.html`](opengrants-os-1.html) (download for offline use; fonts load from Google when online).

Catalog baseline: **August 2026** (illustrative — always verify with the funder).

## Why OpenGOS?

Most funding tools are closed SaaS or fragmented portals. OpenGOS is:

- A **first-class MCP Server** any agent (Claude, Cursor, custom agents) can call
- An **autonomous multi-agent system** for discovery → ranking → drafting → evaluation
- Explicitly optimized for **open-source**, open weights, and **public-goods funding**
- Fully open-source (Apache 2.0), self-hostable, and provenance-first
- Dogfooding itself (see `docs/DOGFOODING_OPENGRANTS.md`)

## Features (v0.2.1)

| Capability | Status |
|------------|--------|
| Live Grants.gov search | ✅ |
| NSF Awards search | ✅ |
| Public-goods / donation sources | ✅ |
| Profile Steward | ✅ |
| Grounded proposal drafting | ✅ |
| Continuous ingestion + evaluation harness | ✅ |
| Ranking with declared open-source bias | ✅ |
| Interactive shell + 3D Constellation | ✅ |

## Quick Start (MCP Server)

```bash
git clone https://github.com/ANAMIZED/opengrants-os.git
cd opengrants-os
pip install -e .
opengos          # or: python -m opengrants
```

### MCP Client Config

```json
{
  "mcpServers": {
    "opengos": {
      "command": "opengos",
      "args": []
    }
  }
}
```

Or:

```json
{
  "mcpServers": {
    "opengos": {
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
| `search_grants` | Live Grants.gov keyword search with provenance |
| `get_grant_details` | Detail view for a specific opportunity |
| `list_open_source_relevant_grants` | Open-source biased discovery |
| `list_public_goods_funding` | Donations, sponsorships, quadratic & open-source funds |
| `search_nsf_awards` | NSF Awards public API |
| `refresh_corpus` | Continuous ingestion into local corpus |
| `run_evaluation` | Discovery + open-source relevance harness |
| `upsert_profile` | Create / update project profile |
| `draft_proposal_outline` | Grounded outline (grants **and** public-goods vehicles) |

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

## Support

- GitHub Sponsors (enable on the account)
- Open Collective (create a collective; update `.github/FUNDING.yml`)
- See `docs/DOGFOODING_OPENGRANTS.md`

## Publishing

- PyPI package name: **`opengos`**
- Official MCP Registry: `server.json` → `io.github.ANAMIZED/opengos`
- Glama: `glama.json`
- GitHub repo path remains `ANAMIZED/opengrants-os` for continuity

## License

Apache License 2.0 — see [LICENSE](LICENSE).

---

**Built for the open-source community.**  
https://github.com/ANAMIZED/opengrants-os
