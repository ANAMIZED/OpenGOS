# OpenGOS

[![CI](https://github.com/ANAMIZED/OpenGOS/actions/workflows/ci.yml/badge.svg)](https://github.com/ANAMIZED/OpenGOS/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Server-purple.svg)](https://modelcontextprotocol.io)
[![SDK](https://img.shields.io/badge/SDK-Python-green.svg)](src/opengos/sdk/)
[![CLI](https://img.shields.io/badge/CLI-opengos--cli-orange.svg)](src/opengos/cli.py)
[![API](https://img.shields.io/badge/API-FastAPI-009688.svg)](src/opengos/api/)

**Autonomous agentic MCP server for grants discovery, ranking, drafting, and public-goods funding.**

**[OpenGOS Pro — $49/mo](https://buy.stripe.com/7sY8wQ5EWf1H3p3bby43S01)** · **[OpenGOS Advanced Search ($0.40)](https://buy.stripe.com/7sY8wQ5EW3iZ5xb5Re43S06)** · **[OpenGOS Proposal Draft ($2.50)](https://buy.stripe.com/9B69AUd7o7zf2kZ2F243S03)** · **[Support Agentic OS Kernels ($99)](https://buy.stripe.com/bJecN63wObPv6Bf7Zm43S02)** · **[Support Public Goods](https://donate.stripe.com/00w5kE3wOg5L8Jn2F243S00)** · **[Consulting Hour ($199)](https://buy.stripe.com/dRmaEYgjA9Hnf7LdjG43S0b)**

### Non-custodial USDC (preferred for agents / x402)

| Network | Address |
|---------|---------|
| **Base / Ethereum** | `0xD3d0E9eDAe3Ac7bb199a8EAA761BdA423b878438` |
| **Solana** | `ETQwWf19axArsY493UfC6bxe2BmEzmzvCb58PPnC38A` |

*Related:* [rui](https://github.com/ANAMIZED/rui) · [LRSI](https://github.com/ANAMIZED/LRSI) · [server-os](https://github.com/ANAMIZED/server-os) · [openmesha](https://github.com/ANAMIZED/openmesha) · [YodMCP](https://github.com/ANAMIZED/YodMCP)

## Surfaces

| Surface | Entry |
|---------|-------|
| **MCP Server** | `opengos` |
| **CLI** | `opengos-cli status` / `search` |
| **SDK** | `from opengos.sdk import OpenGOSClient` |
| **REST API** | `opengos-api` → http://localhost:8080/docs |
| **Multi-agent** | discoverer → ranker → drafter + `skills/multi-agent-workflow/` |
| **Hero demo** | [`opengos.html`](opengos.html) |
| **CI** | `.github/workflows/ci.yml` |

## Quick Start

```bash
pip install -e ".[dev,api]"
opengos          # MCP
opengos-cli status
opengos-api      # REST :8080
```

## License

Apache-2.0
