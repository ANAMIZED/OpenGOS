# OpenGOS Architecture

## Goals

1. Make funding discovery **callable by agents** (MCP-first)
2. Treat **grants and public-goods funding** as equal citizens
3. Keep results **grounded** with provenance
4. Stay **self-hostable** and open (Apache 2.0)

## High-level flow

```
Agent / Client
      │
      ▼
 FastMCP Server  (src/opengos/server.py)
      │
      ├─► Grants.gov client     (grants_client.py)
      ├─► NSF adapter           (sources/nsf.py)
      ├─► Public-goods catalog  (sources/public_goods.py)
      ├─► Profile steward       (profile/steward.py)
      ├─► Drafting              (drafting/drafter.py)
      ├─► Ingestion             (ingestion/corpus.py)
      └─► Evaluation harness    (evaluation/harness.py)
```

## MCP surface

### Tools

- Discovery: `search_grants`, `get_grant_details`, `list_open_source_relevant_grants`, `search_nsf_awards`
- Public goods: `list_public_goods_funding`
- Profile: `upsert_profile`
- Drafting: `draft_proposal_outline`
- Ops: `refresh_corpus`, `run_evaluation`

### Resources

- `opengos://status`
- `opengos://sources`

## Design principles

| Principle | Meaning |
|-----------|--------|
| Provenance first | Source + retrieved_at + official URL on opportunities |
| Declared bias | Ranking prefers open-source / public-interest relevance |
| Public goods parity | Donations and sponsorships are not second-class |
| Grounded drafts | Outlines reference real opportunity data |
| Minimal secrets | Public APIs only by default |

## Interactive shell

`opengos.html` is a standalone browser UI for exploration. It is complementary to the MCP server, not a replacement.

## Extension points

- New source adapters under `src/opengos/sources/`
- New MCP tools in `server.py`
- Ranking / agent logic under `src/opengos/agents/`
- Evaluation cases under `src/opengos/evaluation/`
