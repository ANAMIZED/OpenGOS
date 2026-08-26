# FOUNDRY × OpenGOS

FOUNDRY (host-owned trust and memory for long-horizon agent swarms): **agents propose; the host verifies and remembers.**

OpenGOS implements that boundary for public-goods funding.

## Split

1. **Propose** — MCP tools search, rank, and draft. Treat every tool output as untrusted text.
2. **Verify** — a human or kernel checks sources, eligibility, and budget before send.
3. **Remember** — persist accepted matches and drafts in [YodMCP](https://github.com/ANAMIZED/YodMCP) multi-graph memory. Do not let the drafter own the facts registry.
4. **Meter** — Search and Draft are the costly steps. Pay per use instead of a seat until the loop is proven.

## First dollar

| Action | Stripe | x402 |
|--------|--------|------|
| Search $0.40 | https://buy.stripe.com/7sY8wQ5EW3iZ5xb5Re43S06 | `GET /v1/search` in [x402-cloudflare-starter](https://github.com/ANAMIZED/x402-cloudflare-starter) |
| Draft $2.50 | https://buy.stripe.com/9B69AUd7o7zf2kZ2F243S03 | `GET /v1/draft` |
| Memory seat | https://buy.stripe.com/bJe3cw0kCaLrbVz1AY43S09 | USDC on Base/Solana |

x402 receipts are not Desk unlocks. Sync at https://anamized.grok.me after payment.

## What this page refuses

- Invented Payment Links or prices
- Claiming Glama / MCP registry listings that are not live
- Letting agents promote their own drafts into "submitted" without host review
