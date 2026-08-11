# OpenGrants OS

**The ultimate open-source Autonomous Agentic AI MCP Server for grants discovery, matching, drafting, and lifecycle management — built for open-source AI and public goods.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-Server-purple.svg)](https://modelcontextprotocol.io)
[![Status](https://img.shields.io/badge/Status-MVP-orange.svg)]()
[![GitHub](https://img.shields.io/badge/GitHub-ANAMIZED%2Fopengrants--os-black.svg)](https://github.com/ANAMIZED/opengrants-os)

> **Vision**: Eliminate the discovery tax that disadvantages open-source AI builders. Provide transparent, grounded, autonomous infrastructure so public-goods work can compete for funding on equal footing with closed labs.

## Why OpenGrants OS?

Most grant tooling is either closed SaaS or fragmented portals. OpenGrants OS is:

- A **first-class MCP Server** that any AI agent (Claude, Cursor, custom agents) can call
- An **Autonomous multi-agent Operating System** (LangGraph) for continuous discovery → ranking → drafting → red-teaming → lifecycle
- Explicitly optimized for **open-source AI**, open weights, and public-goods funding
- Fully open-source (Apache 2.0), self-hostable, and provenance-first

## Current Status — v0.1.0 MVP

**Live now**:
- Production-ready MCP Server with real Grants.gov integration
- Tools: `search_grants`, `get_grant_details`, `list_open_source_relevant_grants`
- Strong provenance on every result
- Multi-agent LangGraph scaffold ready for expansion
- Clean packaging and public repository

**Roadmap**:
- Continuous multi-source corpus (NSF, NIH, Horizon Europe, open-source funds…)
- Profile steward (GitHub activity + research statements)
- Full multi-agent ranking, eligibility, open-source alignment scoring
- Proposal drafting + red-team reviewer agents
- Lifecycle tracking + human-in-the-loop submission gates
- Evaluation harness and public benchmarks

## Quick Start

```bash
# Clone
git clone https://github.com/ANAMIZED/opengrants-os.git
cd opengrants-os

# Install (core)
pip install -e .

# Optional: multi-agent extras
pip install -e ".[agents]"

# Run as MCP server (stdio)
python -m opengrants
# or
opengrants
```

### Connect to Claude Desktop / Cursor / any MCP client

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
| `search_grants` | Keyword search against live Grants.gov public API. Returns normalized opportunities with provenance. |
| `get_grant_details` | Detailed view of a specific opportunity by ID. |
| `list_open_source_relevant_grants` | Discovery focused on open-source AI / public-goods relevant funding with lightweight ranking. |

## Resources

- `opengrants://status` — Version, capabilities, roadmap
- `opengrants://sources` — Current and planned data sources

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MCP Interface                         │
│         (tools + resources + prompts)                    │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              OpenGrants OS Core                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │  Discovery  │  │   Ranking   │  │  Drafting +     │  │
│  │  Agents     │→ │  + Profile   │→ │  Red-Team       │  │
│  └─────────────┘  │  Matching   │  │  Agents         │  │
│                   └─────────────┘  └─────────────────┘  │
│                                                          │
│  Continuous ingestion · Provenance · HITL gates          │
└─────────────────────────────────────────────────────────┘
```

The MCP surface stays stable while the internal multi-agent system evolves.

## Development

```bash
pip install -e ".[dev,agents]"
ruff check .
pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Apache License 2.0 — see [LICENSE](LICENSE).

---

**Built for the open-source AI community.**  
Let’s make the funding landscape as open as the code we write.

https://github.com/ANAMIZED/opengrants-os
