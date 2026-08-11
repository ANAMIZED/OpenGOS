# OpenGrants OS

**The ultimate open-source Autonomous Agentic AI MCP Server for grants discovery, matching, drafting, and lifecycle management — built for open-source AI and public goods.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-Server-purple.svg)](https://modelcontextprotocol.io)
[![Version](https://img.shields.io/badge/Version-0.2.0-green.svg)]()
[![GitHub](https://img.shields.io/badge/GitHub-ANAMIZED%2Fopengrants--os-black.svg)](https://github.com/ANAMIZED/opengrants-os)

> **Vision**: Eliminate the discovery tax that disadvantages open-source AI builders. Provide transparent, grounded, autonomous infrastructure so public-goods work can compete for funding on equal footing with closed labs — including traditional grants **and** donation / sponsorship / quadratic public-goods funding.

## What’s New in 0.2.0

- **Public Goods / Donation sources**: GitHub Sponsors, Open Collective, Gitcoin, Sentient, OpenSSF, NumFOCUS, PSF, and more as first-class funding opportunities
- **NSF Awards** search
- **Profile Steward**: create and maintain project/researcher profiles for personalized matching and drafting
- **Drafting agents**: grounded proposal outlines + short pitches for both grants and donation vehicles
- Continuous ingestion + evaluation harness (from 0.1.x)
- Multi-agent ranking with open-source bias

## Quick Start

```bash
git clone https://github.com/ANAMIZED/opengrants-os.git
cd opengrants-os
pip install -e .
python -m opengrants
```

### MCP Client Config (Claude Desktop / Cursor)

```json
{
  "mcpServers": {
    "opengrants": {
      "command": "python",
      "args": ["-m", "opengrants"],
      "cwd": "/path/to/opengrants-os"
    }
  }
}
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `search_grants` | Live Grants.gov keyword search with provenance |
| `get_grant_details` | Detail view for a specific opportunity |
| `list_open_source_relevant_grants` | Open-source / AI biased discovery |
| `list_public_goods_funding` | **Donation, sponsorship, quadratic & open-source funds** |
| `search_nsf_awards` | NSF Awards public API |
| `refresh_corpus` | Continuous ingestion into local corpus |
| `run_evaluation` | Discovery + open-source relevance harness |
| `upsert_profile` | Create / update a project or researcher profile |
| `draft_proposal_outline` | Grounded outline + short pitch for grants **or** public-goods funding |

## Resources

- `opengrants://status`
- `opengrants://sources`

## Why Donation / Gifting Sources?

Many of the most important open-source AI contributions are funded outside traditional government grants — through GitHub Sponsors, Open Collective, Gitcoin quadratic rounds, foundation open-source programs, and direct public-goods funding. OpenGrants OS treats these as **first-class citizens** alongside Grants.gov and agency programs so that maintainers of public-goods AI can discover and apply for the full spectrum of support.

## Architecture

MCP Interface → Discovery (Grants.gov + NSF + Public Goods) → Profile Steward → Ranking Agents → Drafting Agents → Evaluation & Corpus

## Development

```bash
pip install -e ".[dev,agents]"
ruff check .
python -m opengrants.evaluation.harness
```

## Publishing

- **PyPI**: Package is ready (`hatchling`). Publish with `hatch build && twine upload dist/*` once credentials are available.
- **Official MCP Registry**: `server.json` is present. Use `mcp-publisher login github && mcp-publisher publish`.
- **Glama**: `glama.json` is present; claim the listing after indexing.

## License

Apache License 2.0

---

**Built for the open-source AI community.**  
Let’s make the funding landscape as open as the code we write.

https://github.com/ANAMIZED/opengrants-os
