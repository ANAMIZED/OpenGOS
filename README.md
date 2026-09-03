# OpenGOS

[![CI](https://github.com/ANAMIZED/OpenGOS/actions/workflows/ci.yml/badge.svg)](https://github.com/ANAMIZED/OpenGOS/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Server-purple.svg)](https://modelcontextprotocol.io)
[![SDK](https://img.shields.io/badge/SDK-Python-green.svg)](src/opengos/sdk/)
[![CLI](https://img.shields.io/badge/CLI-opengos--cli-orange.svg)](src/opengos/cli.py)
[![API](https://img.shields.io/badge/API-FastAPI-009688.svg)](src/opengos/api/)

**Autonomous agentic MCP server for grants discovery, ranking, drafting, and public-goods funding.**

### Support the work

OpenGOS is funded by donations and sponsorships only. There is no Pro seat, consulting hour, or pay-per-use search/draft SKU.

| Option | Amount | Link |
|--------|--------|------|
| **Public Goods Support** | $25 | [Donate](https://donate.stripe.com/00w5kE3wOg5L8Jn2F243S00) |
| **Monthly Sponsor** | $25/mo | [Sponsor](https://donate.stripe.com/dRm28s4AS5r75xb1AY43S0c) |
| **Kernel Support** | $99 | [Donate](https://buy.stripe.com/bJecN63wObPv6Bf7Zm43S02) |

Demo: [Interactive shell](https://htmlpreview.github.io/?https://github.com/ANAMIZED/OpenGOS/blob/main/opengos.html)

### Non-custodial USDC (preferred for agents / x402)

| Network | Address |
|---------|---------|
| **Base / Ethereum** | `0xD3d0E9eDAe3Ac7bb199a8EAA761BdA423b878438` |
| **Solana** | `ETQwWf19axArsY493UfC6bxe2BmEzmzvCb58PPnC38A` |

*Related:* [RUI](https://github.com/ANAMIZED/Recursive-UltraIntelligence-RUI) · [LRSI](https://github.com/ANAMIZED/LRSI) · [Server-OS](https://github.com/ANAMIZED/Server-OS) · [OpenMesha](https://github.com/ANAMIZED/OpenMesha) · [YodMCP](https://github.com/ANAMIZED/YodMCP) · [desk](https://github.com/ANAMIZED/desk)

## FOUNDRY mapping

FOUNDRY separates untrusted proposal generation from host-owned verification and an established-facts registry. OpenGOS is the grants surface of that split:

| FOUNDRY role | OpenGOS surface |
|--------------|-----------------|
| Agents propose | discoverer → ranker → drafter (`skills/multi-agent-workflow/`) |
| Host verifies | human / kernel review before a proposal is sent |
| Established facts | ranked grant matches + draft artifacts, not self-attested win reports |

Durable memory for those facts lives in [YodMCP](https://github.com/ANAMIZED/YodMCP). Promotion through kernels is fail-closed ([LRSI](https://github.com/ANAMIZED/LRSI), [Server-OS](https://github.com/ANAMIZED/Server-OS), [RUI](https://github.com/ANAMIZED/Recursive-UltraIntelligence-RUI)). Host owns the evaluator; agents propose.

One-page note: [`docs/FOUNDRY.md`](docs/FOUNDRY.md).

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
