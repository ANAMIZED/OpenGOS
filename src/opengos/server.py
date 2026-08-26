"""
OpenGOS — Autonomous Agentic AI MCP Server

Primary entry point. Exposes a clean MCP interface for grants discovery,
public-goods funding, profile stewardship, and grounded drafting.
"""

from __future__ import annotations

import json
import logging
from typing import Annotated, Any

from fastmcp import FastMCP
from pydantic import Field

from opengos.grants_client import GrantOpportunity, get_client
from opengos.tools.hints import tool_hints

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("opengos")

mcp = FastMCP(
    name="OpenGOS",
    instructions=(
        "OpenGOS is an autonomous agentic MCP server specialized in "
        "grant discovery, ranking, eligibility analysis, drafting, and lifecycle support. "
        "It prioritizes open-source software and public-goods funding, including donations, "
        "sponsorships, and quadratic funding vehicles. Every result includes provenance. "
        "Treat public-goods funding as first-class, not secondary to federal grants. "
        "Use search_grants for Grants.gov keyword search; get_grant_details for one opportunity; "
        "list_public_goods_funding / get_public_goods_details for donations and OS funds; "
        "search_nsf_awards for NSF history; upsert_profile then draft_proposal_outline."
    ),
)

_RO = {"read_only": True, "destructive": False, "idempotent": True, "open_world": True}
_RW = {"read_only": False, "destructive": False, "idempotent": True, "open_world": False}
_DEL = {"read_only": False, "destructive": True, "idempotent": True, "open_world": False}


def _serialize(g: GrantOpportunity, include_raw: bool = False) -> dict[str, Any]:
    data = g.model_dump(exclude={"raw"} if not include_raw else set())
    data["open_source_relevant"] = g.is_open_source_relevant
    return data


@mcp.tool(
    name="search_grants",
    title="Search Grants.gov opportunities",
    description=(
        "Search currently posted U.S. federal grant opportunities on Grants.gov by keyword and "
        "return normalized records with source, retrieved_at, official URL, and an open-source "
        "relevance flag. Use this when you need a list of live opportunities. Do not use this "
        "for NSF award history (search_nsf_awards) or donation/sponsorship vehicles "
        "(list_public_goods_funding). Results are public HTTP lookups (open-world, no API key). "
        "Always verify the official source_url before applying. Does not persist state."
    ),
    annotations=tool_hints("Search Grants.gov opportunities", **_RO),
)
async def search_grants(
    keyword: Annotated[str, Field(description="Free-text query sent to Grants.gov (topic, agency, or opportunity number fragment).")],
    max_results: Annotated[int, Field(description="Maximum opportunities to return. Clamped to 1-50. Default 15.")] = 15,
    status: Annotated[str, Field(description="Grants.gov opportunity status filter. Typical value is 'posted'.")] = "posted",
) -> str:
    if not keyword or not keyword.strip():
        return json.dumps({"error": "keyword is required"}, indent=2)
    client = await get_client()
    results = await client.search(keyword=keyword.strip(), rows=min(max(max_results, 1), 50), opp_statuses=status)
    payload = {
        "query": keyword,
        "status_filter": status,
        "count": len(results),
        "retrieved_at": results[0].retrieved_at if results else None,
        "opportunities": [_serialize(g) for g in results],
        "notes": "Results normalized from public Grants.gov data. Always verify official source_url.",
    }
    return json.dumps(payload, indent=2, default=str)


@mcp.tool(
    name="get_grant_details",
    title="Get one Grants.gov opportunity",
    description=(
        "Retrieve a single Grants.gov opportunity by id or opportunity number, including raw "
        "source fields and provenance (source, retrieved_at, official_url). Use after "
        "search_grants when you need the full record for eligibility or drafting. Not for NSF "
        "awards (search_nsf_awards) or public-goods catalog items (get_public_goods_details). "
        "Open-world public lookup; if several records match, the first exact id/number wins."
    ),
    annotations=tool_hints("Get one Grants.gov opportunity", **_RO),
)
async def get_grant_details(
    opportunity_id: Annotated[str, Field(description="Grants.gov opportunity id or opportunity number from search_grants.")],
) -> str:
    if not opportunity_id or not opportunity_id.strip():
        return json.dumps({"error": "opportunity_id is required"}, indent=2)
    client = await get_client()
    results = await client.search(keyword=opportunity_id.strip(), rows=15)
    match = None
    oid = opportunity_id.strip()
    for g in results:
        if g.id == oid or (g.opportunity_number and oid in str(g.opportunity_number)):
            match = g
            break
    if not match and results:
        match = results[0]
    if not match:
        return json.dumps({"error": "Opportunity not found", "opportunity_id": opportunity_id}, indent=2)
    return json.dumps({"opportunity": _serialize(match, include_raw=True), "provenance": {"source": match.source, "retrieved_at": match.retrieved_at, "official_url": match.source_url}}, indent=2, default=str)


@mcp.tool(
    name="list_open_source_relevant_grants",
    title="List open-source-biased Grants.gov hits",
    description=(
        "Discover Grants.gov opportunities ranked with a declared open-source / public-goods "
        "bias. Runs several related keyword searches, dedupes by id, and sorts open-source-"
        "relevant records first. Use when the user wants funding for OSS rather than a raw "
        "keyword dump (search_grants). Does not cover donations (list_public_goods_funding)."
    ),
    annotations=tool_hints("List open-source-biased Grants.gov hits", **_RO),
)
async def list_open_source_relevant_grants(
    focus: Annotated[str, Field(description="Primary focus phrase mixed into the search set.")] = "open source artificial intelligence",
    max_results: Annotated[int, Field(description="Maximum ranked opportunities to return. Default 12.")] = 12,
) -> str:
    keywords = [focus, "open source artificial intelligence", "open weight models", "public interest technology", "open source software"]
    client = await get_client()
    seen: set[str] = set()
    pooled: list[GrantOpportunity] = []
    for kw in keywords:
        batch = await client.search(keyword=kw, rows=max_results)
        for g in batch:
            if g.id not in seen:
                seen.add(g.id)
                pooled.append(g)
    ranked = sorted(pooled, key=lambda g: (g.is_open_source_relevant, g.close_date or ""), reverse=True)[:max_results]
    return json.dumps({"focus": focus, "count": len(ranked), "open_source_bias": True, "opportunities": [_serialize(g) for g in ranked]}, indent=2, default=str)


@mcp.tool(
    name="list_public_goods_funding",
    title="List public-goods funding vehicles",
    description=(
        "List curated public-goods funding vehicles: GitHub Sponsors, Open Collective, Gitcoin "
        "quadratic rounds, NLnet, Sovereign Tech Agency, OpenSSF, NumFOCUS, PSF, and similar. "
        "Use this for donations and OS funds — not live Grants.gov postings (search_grants) or "
        "NSF award history (search_nsf_awards). Call get_public_goods_details for one vehicle."
    ),
    annotations=tool_hints("List public-goods funding vehicles", read_only=True, destructive=False, idempotent=True, open_world=False),
)
async def list_public_goods_funding(
    max_results: Annotated[int, Field(description="Maximum catalog items to return. Default 25.")] = 25,
) -> str:
    try:
        from opengos.sources.public_goods import list_catalog
        items = list_catalog()
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)
    return json.dumps({"count": min(len(items), max_results), "items": items[:max_results], "notes": "Includes donations and sponsorship vehicles as first-class funding paths."}, indent=2, default=str)


@mcp.tool(
    name="get_public_goods_details",
    title="Get one public-goods funding vehicle",
    description=(
        "Return one curated public-goods funding vehicle by catalog id (e.g. pg-nlnet) or title "
        "substring, including URL, type, focus_areas, and notes. Use after "
        "list_public_goods_funding. This is not a live Grants.gov or NSF lookup."
    ),
    annotations=tool_hints("Get one public-goods funding vehicle", read_only=True, destructive=False, idempotent=True, open_world=False),
)
async def get_public_goods_details(
    item_id: Annotated[str, Field(description="Catalog id from list_public_goods_funding (e.g. 'pg-github-sponsors') or a title substring.")],
) -> str:
    try:
        from opengos.sources.public_goods import get_item
        item = get_item(item_id)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)
    if not item:
        return json.dumps({"error": "public-goods item not found", "item_id": item_id}, indent=2)
    return json.dumps({"item": item}, indent=2, default=str)


@mcp.tool(
    name="search_nsf_awards",
    title="Search NSF Awards API",
    description=(
        "Search the public NSF Awards API for historical and active research awards matching a "
        "keyword. Use for NSF history, not live Grants.gov opportunities (search_grants) or "
        "donation vehicles (list_public_goods_funding). Open-world public HTTP; no auth."
    ),
    annotations=tool_hints("Search NSF Awards API", **_RO),
)
async def search_nsf_awards(
    keyword: Annotated[str, Field(description="NSF Awards API keyword (topic, directorate, institution, or award fragment).")],
    max_results: Annotated[int, Field(description="Maximum awards to return. Default 15.")] = 15,
) -> str:
    try:
        from opengos.sources.nsf import search_nsf
        results = await search_nsf(keyword=keyword, limit=max_results)
    except Exception as e:
        return json.dumps({"error": str(e), "hint": "NSF public API may be temporarily unavailable"}, indent=2)
    return json.dumps({"query": keyword, "count": len(results), "awards": results}, indent=2, default=str)


@mcp.tool(
    name="refresh_corpus",
    title="Refresh local funding corpus",
    description=(
        "Re-pull configured sources into the local OpenGOS corpus used by ranking and drafting. "
        "Use when search results look stale. Writes local cache files; does not mutate Grants.gov. "
        "Not a search tool — call search_grants afterwards."
    ),
    annotations=tool_hints("Refresh local funding corpus", read_only=False, destructive=False, idempotent=True, open_world=True),
)
async def refresh_corpus() -> str:
    try:
        from opengos.ingestion.corpus import refresh
        stats = await refresh()
        return json.dumps({"status": "ok", "stats": stats}, indent=2, default=str)
    except Exception as e:
        return json.dumps({"status": "partial", "error": str(e)}, indent=2)


@mcp.tool(
    name="run_evaluation",
    title="Run discovery evaluation harness",
    description=(
        "Run the built-in discovery / open-source-relevance evaluation harness and return a "
        "JSON report. Use for regression checks, not for finding a grant for a user. "
        "Read-mostly; may hit public APIs. No profile or corpus mutation."
    ),
    annotations=tool_hints("Run discovery evaluation harness", read_only=True, destructive=False, idempotent=True, open_world=True),
)
async def run_evaluation() -> str:
    try:
        from opengos.evaluation.harness import run
        report = await run()
        return json.dumps(report, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool(
    name="upsert_profile",
    title="Create or update project profile",
    description=(
        "Create or overwrite the in-memory project profile used by ranking and "
        "draft_proposal_outline. Id is a slug of name. Use before drafting. In-memory only "
        "(lost on restart). See list_profiles / get_profile / delete_profile for the rest of CRUD."
    ),
    annotations=tool_hints("Create or update project profile", **_RW),
)
async def upsert_profile(
    name: Annotated[str, Field(description="Human project name. Also used to derive the profile id slug.")],
    pitch: Annotated[str, Field(description="Short project description used as ranking/drafting context.")] = "",
    tags: Annotated[str, Field(description="Comma-separated focus tags (e.g. 'open-source,ai,security').")] = "open-source",
) -> str:
    try:
        from opengos.profile.steward import upsert
        profile = upsert(name=name, pitch=pitch, tags=[t.strip() for t in tags.split(",") if t.strip()])
        return json.dumps({"status": "ok", "profile": profile}, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool(
    name="get_profile",
    title="Get a project profile",
    description=(
        "Read one in-memory project profile by name or slug created via upsert_profile. Use "
        "before draft_proposal_outline to confirm pitch/tags. Returns an error object if missing."
    ),
    annotations=tool_hints("Get a project profile", read_only=True, destructive=False, idempotent=True, open_world=False),
)
async def get_profile(
    name: Annotated[str, Field(description="Profile name or slug previously passed to upsert_profile.")],
) -> str:
    from opengos.profile.steward import get_profile as _get
    return json.dumps(_get(name), indent=2, default=str)


@mcp.tool(
    name="list_profiles",
    title="List project profiles",
    description=(
        "List all in-memory project profiles stored by upsert_profile in this process. Use to "
        "discover slugs before get_profile or delete_profile. Empty list if none since startup."
    ),
    annotations=tool_hints("List project profiles", read_only=True, destructive=False, idempotent=True, open_world=False),
)
async def list_profiles() -> str:
    from opengos.profile.steward import list_profiles as _list
    items = _list()
    return json.dumps({"count": len(items), "profiles": items}, indent=2, default=str)


@mcp.tool(
    name="delete_profile",
    title="Delete a project profile",
    description=(
        "Permanently remove one in-memory project profile by name or slug. Destructive. Use "
        "when a profile should no longer ground drafts. Prefer get_profile first to confirm."
    ),
    annotations=tool_hints("Delete a project profile", **_DEL),
)
async def delete_profile(
    name: Annotated[str, Field(description="Profile name or slug to delete from the in-memory steward.")],
) -> str:
    from opengos.profile.steward import delete_profile as _delete
    return json.dumps(_delete(name), indent=2, default=str)


@mcp.tool(
    name="draft_proposal_outline",
    title="Draft a grounded proposal outline",
    description=(
        "Build a grounded proposal outline for a Grants.gov opportunity id or a public-goods "
        "vehicle id, using the current upsert_profile when present. Does not submit applications. "
        "Treat output as a draft requiring human review. May look up the opportunity (open-world)."
    ),
    annotations=tool_hints("Draft a grounded proposal outline", read_only=True, destructive=False, idempotent=True, open_world=True),
)
async def draft_proposal_outline(
    opportunity_id: Annotated[str, Field(description="Grants.gov opportunity id/number or public-goods catalog id.")],
    project_name: Annotated[str, Field(description="Optional project name override. Empty uses the stored profile name.")] = "",
) -> str:
    try:
        from opengos.drafting.drafter import outline
        draft = await outline(opportunity_id=opportunity_id, project_name=project_name or None)
        return json.dumps(draft, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.resource("opengos://status")
def status() -> str:
    return json.dumps({"name": "OpenGOS", "version": "0.5.0", "transport": "stdio", "philosophy": "Public-good first. Strong provenance. Declared open-source ranking bias."}, indent=2)


@mcp.resource("opengos://sources")
def data_sources() -> str:
    return json.dumps({"primary": [{"name": "Grants.gov", "auth_required": False}, {"name": "NSF Awards API", "auth_required": False}], "public_goods": ["GitHub Sponsors", "Open Collective", "Gitcoin", "OpenSSF", "NumFOCUS", "PSF", "NLnet", "Sovereign Tech Agency"]}, indent=2)


def main() -> None:
    logger.info("Starting OpenGOS MCP Server v0.5.0")
    mcp.run()


if __name__ == "__main__":
    main()
