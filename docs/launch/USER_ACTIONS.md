# User Actions Checklist (post expert review)

## Critical decisions

- [ ] **Name:** Keep “OpenGrants OS” only after legal clearance, or rename (GrantConstellation / PublicGoods OS / LedgerGrants / …) **before** PyPI publish
- [ ] Upload **v0.2.1** demo HTML (`opengrants-os-1.html`) from local artifacts after P0 fixes

## Publishing (credentials required)

- [ ] PyPI: `twine upload dist/*` with API token
- [ ] Official MCP Registry: `mcp-publisher publish`
- [ ] Glama: claim + list server
- [ ] GitHub Pages: Settings → Pages → Source = GitHub Actions

## Product follow-ups

- [ ] Live Grants.gov / NSF ingestion as primary surface
- [ ] Sheet focus trap + Constellation text fallback
- [ ] Draft editor exempt from full `refresh()`
