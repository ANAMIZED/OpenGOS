# Remaining User Actions (5–15 minutes each)

These steps require your personal login / credentials. Everything else is already prepared in the repo.

## 1. Apply GitHub Topics (≈ 1 minute)
1. Go to https://github.com/ANAMIZED/opengrants-os
2. Click the gear icon next to “About”
3. Add these topics (copy-paste):
   ```
   mcp
   model-context-protocol
   grants
   open-source
   ai
   agentic
   public-goods
   funding
   langgraph
   open-weight
   ```
4. Save

## 2. Enable GitHub Sponsors
1. Visit https://github.com/sponsors
2. Join / enable Sponsors for the ANAMIZED account (or create an organization and transfer the repo)
3. Complete the profile + any required tax/bank details
4. Once live, the Sponsor button will appear on the repo (FUNDING.yml is already present)

## 3. Create Open Collective
1. Go to https://opencollective.com/create
2. Choose “Open Source” and follow the verification flow (Open Source Collective fiscal host is recommended)
3. After creation, edit `.github/FUNDING.yml` and set:
   ```yaml
   open_collective: your-collective-slug
   ```

## 4. Publish to Official MCP Registry
```bash
# Install the publisher
curl -L "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/').tar.gz" | tar xz mcp-publisher
sudo mv mcp-publisher /usr/local/bin/

cd /path/to/opengrants-os
mcp-publisher login github   # opens browser for GitHub OAuth
mcp-publisher publish        # uses the server.json already in the repo
```

## 5. Publish to PyPI
```bash
pip install hatch twine
hatch build
twine upload dist/*          # requires your PyPI token
```

## 6. Claim on Glama
- `glama.json` with maintainers is already committed.
- Once Glama indexes the repo (or after you submit via “Add MCP Server”), click “Login with GitHub to claim”.

## 7. Remaining Directories
- PulseMCP: https://www.pulsemcp.com/submit (or wait for Official Registry ingest)
- mcp.so: https://mcp.so/submit
- awesome-mcp-servers: open a PR after Glama listing exists

## 8. Ship the Demo + Launch Posts
- Use `docs/launch/DEMO_SCRIPT.md` to record a 60–90s screen capture
- Copy posts from `docs/launch/LAUNCH_POSTS.md`
