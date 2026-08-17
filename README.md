# OpenGOS

**Autonomous agentic MCP server for grants discovery, ranking, drafting, and public-goods funding.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-Server-purple.svg)](https://modelcontextprotocol.io)
[![Version](https://img.shields.io/badge/Version-0.4.0-green.svg)]()
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)]()
[![GitHub](https://img.shields.io/badge/GitHub-ANAMIZED%2FOpenGOS-black.svg)](https://github.com/ANAMIZED/OpenGOS)

> Eliminate the discovery tax. Treat traditional grants **and** donations / sponsorships / quadratic funding as equal first-class citizens so open-source projects can compete on a level playing field.

**[OpenGOS Pro — $49/mo](https://buy.stripe.com/test_9B65kD60D31e3WVaPVbAs01)** · **[Support Public Goods](https://donate.stripe.com/test_28E8wP60D9pC9hf1flbAs00)**

---

## 🚀 Try it in 10 seconds (Hero Demo)

**[Launch the interactive shell →](https://htmlpreview.github.io/?https://github.com/ANAMIZED/OpenGOS/blob/main/opengos.html)**

No install. Browser-only. Discover · Constellation · Pipeline · Draft · Profile.

*Related:* [LRSI](https://github.com/ANAMIZED/LRSI) (recursive self-improvement kernel) · [server-os](https://github.com/ANAMIZED/server-os) (agent process runtime) · [x402-cloudflare-starter](https://github.com/ANAMIZED/x402-cloudflare-starter) (agent micropayments)

---

## Why OpenGOS?

| Problem | OpenGOS approach |
|---------|------------------|
| Grant discovery is slow and fragmented | Live Grants.gov + NSF + public-goods catalog in one MCP interface |
| Open-source projects are under-served by traditional grants | Explicit open-source ranking bias |
| Donations/sponsorships treated as second-class | Public-goods funding is a first-class citizen |
| Agents can't easily call funding tools | Native **MCP server** any agent can use |
| Drafts are ungrounded | Proposal outlines tied to real opportunities + provenance |

---

## Features

| Capability | Status |
|------------|--------|
| Live Grants.gov search | ✅ |
| NSF Awards search | ✅ |
| Public-goods / donation sources | ✅ |
| Profile Steward | ✅ |
| Grounded proposal drafting | ✅ |
| Continuous ingestion + evaluation | ✅ |
| Open-source biased ranking | ✅ |
| Interactive HTML shell + 3D graph | ✅ |
| Agent-native (`AGENTS.md` + `SKILL.md` + MCP) | ✅ |

---

## Install & Run (MCP Server)

### From source (recommended while alpha)

```bash
git clone https://github.com/ANAMIZED/OpenGOS.git
cd OpenGOS
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
opengos
```

### Module form

```bash
python -m opengos
```

### MCP client config

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
      "args": ["-m", "opengos"],
      "cwd": "/absolute/path/to/OpenGOS"
    }
  }
}
```

---

## MCP Tools

| Tool | Description |
|------|-------------|
| `search_grants` | Live Grants.gov keyword search with provenance |
| `get_grant_details` | Detail view for a specific opportunity |
| `list_open_source_relevant_grants` | Open-source biased discovery |
| `list_public_goods_funding` | Donations, sponsorships, quadratic & OS funds |
| `search_nsf_awards` | NSF Awards public API |
| `refresh_corpus` | Continuous ingestion into local corpus |
| `run_evaluation` | Discovery + open-source relevance harness |
| `upsert_profile` | Create / update project profile |
| `draft_proposal_outline` | Grounded outline (grants and public-goods vehicles) |

### MCP Resources

| Resource | Description |
|----------|-------------|
| `opengos://status` | Server name, version, philosophy |
| `opengos://sources` | Data sources and public-goods catalog |

---

## Architecture

```
MCP Interface (FastMCP)
        ↓
┌────────────────────────────────────────┐
│  Discovery                            │
│  Grants.gov · NSF · Public-Goods      │
└────────────────────────────────────────┘
        ↓
Profile Steward → Ranking → Drafting
        ↓
Evaluation & Continuous Corpus
```

Every opportunity carries **provenance**: source, retrieved_at, official URL.

---

## Agent discoverability

| File | Purpose |
|------|--------|
| `AGENTS.md` | Conventions and boundaries for coding agents |
| `SKILL.md` | Skill description for agent skill discovery |
| `server.json` | MCP registry metadata |
| `glama.json` | Glama MCP index metadata |

---

## Development

```bash
pip install -e ".[dev,agents]"
ruff check src
ruff format src
```

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Publishing

| Channel | Identifier |
|---------|------------|
| PyPI | `opengos` |
| MCP Registry | `io.github.ANAMIZED/opengos` |
| Glama | `glama.json` |

---

## License

Apache License 2.0 — see [LICENSE](LICENSE).

---

Built for open-source AI, public goods, and the agentic funding stack.

https://github.com/ANAMIZED/OpenGOS
