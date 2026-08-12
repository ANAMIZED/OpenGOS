# Rename: OpenGrants OS → OpenGOS

**Effective:** 2026-08-12 (v0.2.1)

## Why

Expert review and market check confirmed a direct name collision with the commercial **OpenGrants** product (opengrants.io / mcp.opengrants.io), which operates in the same grant-discovery market and already offers a Claude MCP connector.

## What changed

| Surface | Value |
|---------|--------|
| Product name | **OpenGOS** |
| PyPI package | `opengos` |
| MCP registry name | `io.github.ANAMIZED/opengos` |
| CLI entry points | `opengos` (primary), `opengrants` (compat alias) |
| Python import path | still `opengrants` (internal; may become `opengos` later) |
| GitHub repository | `ANAMIZED/opengrants-os` (unchanged URL for continuity) |

## Optional follow-ups

- [ ] Rename GitHub repo to `opengos` (breaks old links; use GitHub redirect)
- [ ] Rename Python package directory `src/opengrants` → `src/opengos`
- [ ] Update dogfooding docs titles
- [ ] Re-upload demo HTML with OpenGOS branding (local v0.2.1 ready)
