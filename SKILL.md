---
name: opengos
description: >-
  Autonomous agentic MCP server for grants discovery, ranking, drafting, and
  public-goods funding. Searches Grants.gov and NSF, lists sponsorships and
  open-source funds, manages project profiles, and drafts grounded proposal
  outlines. Optimized for open-source AI and public goods. Use when the user
  needs funding discovery, grant matching, proposal outlines, or public-goods
  funding options for open-source projects.
license: Apache-2.0
metadata:
  author: ANAMIZED
  repository: https://github.com/ANAMIZED/OpenGOS
  version: "0.4.0"
  mcp: true
---

# OpenGOS Skill

## When to use this skill

Use OpenGOS when you need to:

- Discover U.S. federal grants (Grants.gov) relevant to a project
- Search NSF awards
- Find public-goods funding (GitHub Sponsors, Open Collective, Gitcoin, OpenSSF, NumFOCUS, NLnet, etc.)
- Rank opportunities with an explicit open-source bias
- Maintain a project funding profile
- Draft a grounded proposal outline for a grant or funding vehicle

## How to run the MCP server

```bash
pip install opengos
# or from source:
pip install -e .

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

## Core tools

| Tool | Purpose |
|------|--------|
| `search_grants` | Keyword search on Grants.gov |
| `get_grant_details` | Details for one opportunity |
| `list_open_source_relevant_grants` | Open-source biased discovery |
| `list_public_goods_funding` | Donations, sponsors, quadratic, OS funds |
| `search_nsf_awards` | NSF Awards API |
| `upsert_profile` | Create/update project profile |
| `draft_proposal_outline` | Grounded outline for a vehicle |
| `refresh_corpus` | Refresh local corpus |
| `run_evaluation` | Run evaluation harness |

## Principles

1. **Provenance first** — every result should carry source + timestamp + official URL
2. **Public goods are first-class** — not an afterthought vs federal grants
3. **Declared open-source bias** — ranking prefers OSS / public-interest relevance
4. **Grounded drafting** — outlines should reference real opportunity data

## Interactive shell

No install required:

https://htmlpreview.github.io/?https://github.com/ANAMIZED/OpenGOS/blob/main/opengos.html
