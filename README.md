# OpenGOS

**Open-source Autonomous Agentic AI MCP Server for grants, public-goods funding, and open-source sustainability.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-Server-purple.svg)](https://modelcontextprotocol.io)
[![Version](https://img.shields.io/badge/Version-0.3-green.svg)]()
[![GitHub](https://img.shields.io/badge/GitHub-ANAMIZED%2FOpenGOS-black.svg)](https://github.com/ANAMIZED/OpenGOS)

> Eliminate the discovery tax. Treat traditional grants **and** donations / sponsorships / quadratic funding as equal first-class citizens so open-source projects can compete on a level playing field.

## Try it now

**[Launch the interactive shell →](https://htmlpreview.github.io/?https://github.com/ANAMIZED/OpenGOS/blob/main/opengos.html)**

Discover · Constellation (3D knowledge graph) · Pipeline · Draft · Console · Profile — one HTML file. No install required.

Source: [`opengos.html`](opengos.html)

Catalog baseline: **August 2026** (illustrative — always verify with the funder).

## Why OpenGOS?

- A **first-class MCP Server** any agent (Claude, Cursor, custom agents) can call
- Discovery → ranking → drafting → evaluation with a **declared open-source bias**
- **Public-goods funding** (sponsors, collectives, quadratic) as first-class citizens
- Apache 2.0, self-hostable, provenance-first

## Features (v0.3)

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
git clone https://github.com/ANAMIZED/OpenGOS.git
cd OpenGOS
pip install -e .
opengos
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

Or via module:

```json
{
  "mcpServers": {
    "opengos": {
      "command": "python",
      "args": ["-m", "opengrants"],
      "cwd": "/absolute/path/to/OpenGOS"
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
| `draft_proposal_outline` | Grounded outline (grants and public-goods vehicles) |

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

- GitHub Sponsors
- Open Collective (update `.github/FUNDING.yml` with your slug)
- See `docs/DOGFOODING.md`

## Publishing

- PyPI: **`opengos`**
- MCP Registry: `io.github.ANAMIZED/opengos`
- Glama: `glama.json`

## License

Apache License 2.0 — see [LICENSE](LICENSE).

---

https://github.com/ANAMIZED/OpenGOS
