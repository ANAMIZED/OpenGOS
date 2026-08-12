# Response to Expert Review (OpenGrants OS demo v0.2 → v0.2.1)

**Date:** 2026-08-12  
**Scope:** Analysis of the external expert review + immediate product/demo updates.

## Verdict on the review

The review is **high quality and mostly correct** on product design, data volatility, competitive landscape, and MCP accuracy. One major external claim is **wrong**: the repository **does exist** and is public.

| Review claim | Our finding |
|--------------|-------------|
| Repo `github.com/ANAMIZED/opengrants-os` unverifiable / fictional | **False.** Public repo exists; reviewer’s search/indexing gap. |
| Name collision with commercial OpenGrants (opengrants.io) | **True.** Same market; rename risk is real. |
| Catalog ~half stale (POSE, DHAG, NGI Zero Core, Prototype Fund, etc.) | **True** as of Aug 2026. |
| P0: `hashchange` blanks screen on unknown hash | **True.** Fixed in v0.2.1. |
| P0: “offline-capable” vs Google Fonts CDN | **True.** Claim softened in v0.2.1. |
| MCP mental model accurate | **True.** |
| Concept not novel; differentiators = open-source bias + eval harness | **Agreed.** |
| Match score is heuristic, not “agents” | **True.** UI copy clarified. |

## Immediate updates shipped (demo v0.2.1)

1. **P0 hash router** — `hashchange` now uses the same `VIEWS` whitelist as `nav()`; unknown hashes fall back to Home.
2. **Offline claim** — No longer claims offline-capable; notes fonts load when online.
3. **Catalog re-baseline (Aug 2026)**
   - POSE → **PESOSE** (NSF 26-506), URL + security tags
   - DHAG → marked **historical**; FY2026 rounds not running
   - NGI Zero Core → **NLnet / Open Internet Stack (post-NGI Zero)** with pause/status note
   - Prototype Fund → relaunch amounts (€47.5k–€158k) and annual window note
4. **Honesty**
   - About: “Catalog baseline: August 2026”
   - Profile: match scores described as transparent heuristic
5. **Version** — shell bumped to v0.2.1

## Name strategy (highest strategic risk)

Commercial **OpenGrants** (opengrants.io / ops.opengrants.io / mcp.opengrants.io) is live in grant discovery + Claude MCP connector. Continuing under “OpenGrants OS” invites confusion and possible trademark pressure.

**Recommended directions (pick one before heavy marketing):**

| Candidate | Notes |
|-----------|--------|
| **GrantConstellation** | Matches the demo’s strongest visual metaphor |
| **PublicGoods OS** / **PG-OS** | Emphasizes differentiator (donations + grants) |
| **OpenFunding OS** | Descriptive; check collisions |
| **LedgerGrants** | Fits banknote/ledger design language |
| Keep **OpenGrants OS** only with legal clearance | Assume collision until cleared |

Package name on PyPI is currently `opengrants-os` — renaming later is painful; decide before first successful PyPI publish if possible.

## What the review got right (product prioritization)

1. **Declared open-source ranking bias + evaluation harness** are the real differentiators — keep them first-class in the MCP server, not only in the demo.
2. **Wire live sources** (Grants.gov / Simpler.Grants.gov, NSF, curated public-goods catalog) so the demo’s illustrative numbers stop being the product surface.
3. **Accessibility finish** — focus trap on sheet, non-visual Constellation list, slightly larger mono labels.
4. **Draft view** — exempt from blanket `refresh()` or preserve selection.

## Repo / MCP truthfulness

- MCP server source **exists** under `src/opengrants/` (FastMCP, tools, public-goods sources).
- It is **runnable from source**, not yet published to PyPI / official MCP Registry / Glama.
- Demo About text should not over-claim “live production MCP” until those publishes land.

## Next ordered actions

1. Decide rename vs legal-clear “OpenGrants OS”.
2. Commit v0.2.1 HTML to repo root + `demo/index.html` (local path: artifacts).
3. Publish PyPI when token available → `mcp-publisher publish` → Glama.
4. Extend live ingestion; drop reliance on static catalog for the real server.
5. P1 a11y + draft-focus fixes in a follow-up shell revision.
