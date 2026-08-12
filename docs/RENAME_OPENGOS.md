# Rename: OpenGrants OS → OpenGOS

**Effective:** 2026-08-12 (v0.2.1)

## Package (done)

| Surface | Value |
|---------|--------|
| Product name | **OpenGOS** |
| PyPI / dist | `opengos-0.2.1` (wheel + sdist built) |
| MCP registry name | `io.github.ANAMIZED/opengos` |
| CLI | `opengos` (+ `opengrants` alias) |

## GitHub repository rename (you must click once)

The connected GitHub tools cannot rename a repository. Do this in the UI (takes ~15 seconds):

1. Open https://github.com/ANAMIZED/opengrants-os/settings
2. **Repository name** → change to **`opengos`**
3. Click **Rename**

GitHub keeps automatic redirects from `opengrants-os` → `opengos` for clones, issues, and stars.

After rename, canonical URL is:

**https://github.com/ANAMIZED/opengos**

## Dist artifacts (local)

```
dist/opengos-0.2.1-py3-none-any.whl
dist/opengos-0.2.1.tar.gz
```

Publish when ready:

```bash
twine upload dist/*
# username: __token__
# password: pypi-...
```
