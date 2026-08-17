# OpenGOS

**Autonomous agentic MCP server for grants discovery, ranking, drafting, and public-goods funding.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-Server-purple.svg)](https://modelcontextprotocol.io)
[![Version](https://img.shields.io/badge/Version-0.4.0-green.svg)]()
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)]()
[![GitHub](https://img.shields.io/badge/GitHub-ANAMIZED%2FOpenGOS-black.svg)](https://github.com/ANAMIZED/OpenGOS)

> Eliminate the discovery tax. Treat traditional grants **and** donations / sponsorships / quadratic funding as equal first-class citizens so open-source projects can compete on a level playing field.

**[OpenGOS Pro — $49/mo](https://buy.stripe.com/7sY8wQ5EWf1H3p3bby43S01)** · **[Support Agentic OS Kernels ($99)](https://buy.stripe.com/bJecN63wObPv6Bf7Zm43S02)** · **[Support Public Goods](https://donate.stripe.com/00w5kE3wOg5L8Jn2F243S00)**

### Non-custodial USDC (preferred for agents)

| Network | Address | Explorer |
|---------|---------|----------|
| **Base** | `0xD3d0E9eDAe3Ac7bb199a8EAA761BdA423b878438` | [basescan](https://basescan.org/address/0xD3d0E9eDAe3Ac7bb199a8EAA761BdA423b878438) |
| **Ethereum** | `0xD3d0E9eDAe3Ac7bb199a8EAA761BdA423b878438` | [etherscan](https://etherscan.io/address/0xD3d0E9eDAe3Ac7bb199a8EAA761BdA423b878438) |
| **Solana** | `ETQwWf19axArsY493UfC6bxe2BmEzmzvCb58PPnC38A` | [solscan](https://solscan.io/account/ETQwWf19axArsY493UfC6bxe2BmEzmzvCb58PPnC38A) |

---

## 🚀 Try it in 10 seconds (Hero Demo)

**[Launch the interactive shell →](https://htmlpreview.github.io/?https://github.com/ANAMIZED/OpenGOS/blob/main/opengos.html)**

No install. Browser-only. Discover · Constellation · Pipeline · Draft · Profile.

*Related:* [rui](https://github.com/ANAMIZED/rui) · [LRSI](https://github.com/ANAMIZED/LRSI) · [server-os](https://github.com/ANAMIZED/server-os) · [openmesha](https://github.com/ANAMIZED/openmesha) · [x402-cloudflare-starter](https://github.com/ANAMIZED/x402-cloudflare-starter)

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

```bash
git clone https://github.com/ANAMIZED/OpenGOS.git
cd OpenGOS
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
opengos
```

MCP client config:

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

## License

Apache License 2.0 — see [LICENSE](LICENSE).

Built for open-source AI, public goods, and the agentic funding stack.

https://github.com/ANAMIZED/OpenGOS
