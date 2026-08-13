"""
OpenGOS — Autonomous Agentic AI MCP Server

Primary entry point. Exposes a clean MCP interface for grants discovery,
public-goods funding, profile stewardship, and grounded drafting.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from fastmcp import FastMCP

from opengos.grants_client import GrantOpportunity, get_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("opengos")

mcp = FastMCP(
    name="OpenGOS",
    instructions=(
        "OpenGOS is an autonomous agentic MCP server specialized in "
        "grant discovery, ranking, eligibility analysis, drafting, and lifecycle support. "
        "It prioritizes open-source software and public-goods funding, including donations, "
        "sponsorships, and quadratic funding vehicles. Every result includes provenance. "
        "Treat public-goods funding as first-class, not secondary to federal grants."
    ),
)


def _serialize(g: GrantOpportunity, include_raw: bool = False) -> dict[str, Any]:
    data = g.model_dump(exclude={"raw"} if not include_raw else set())
    data["open_source_relevant"] = g.is_open_source_relevant
    return data


@mcp.tool
async def search_grants(keyword: str, max_results: int = 15, status: str = "posted") -> str:
    """Search open U.S. federal grant opportunities (Grants.gov) by keyword with provenance.

    Returns normalized opportunities including source, retrieved_at, and official URL.
    Always verify details on the official source_url before acting.
    """
    if not keyword or not keyword.strip():
        return json.dumps({"error": "keyword is required"}, indent=2)
    client = await get_client()
    results = await client.search(
        keyword=keyword.strip(), rows=min(max(max_results, 1), 50), opp_statuses=status
    )
    payload = {
        "query": keyword,
        "status_filter": status,
        "count": len(results),
        "retrieved_at": results[0].retrieved_at if results else None,
        "opportunities": [_serialize(g) for g in results],
        "notes": "Results normalized from public Grants.gov data. Always verify official source_url.",
    }
    return json.dumps(payload, indent=2, default=str)


@mcp.tool
async def get_grant_details(opportunity_id: str) -> str:
    """Retrieve details for a specific grant opportunity by ID or opportunity number."""
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
        return json.dumps(
            {"error": "Opportunity not found", "opportunity_id": opportunity_id}, indent=2
        )
    return json.dumps(
        {
            "opportunity": _serialize(match, include_raw=True),
            "provenance": {
                "source": match.source,
                "retrieved_at": match.retrieved_at,
                "official_url": match.source_url,
            },
        },
        indent=2,
        default=str,
    )


@mcp.tool
async def list_open_source_relevant_grants(
    focus: str = "open source artificial intelligence", max_results: int = 12
) -> str:
    """Discover grants particularly relevant to open-source software and public goods."""
    keywords = [
        focus,
        "open source artificial intelligence",
        "open weight models",
        "public interest technology",
        "open source software",
    ]
    client = await get_client()
    seen: set[str] = set()
    pooled: list[GrantOpportunity] = []
    for kw in keywords:
        batch = await client.search(keyword=kw, rows=max_results)
        for g in batch:
            if g.id not in seen:
                seen.add(g.id)
                pooled.append(g)
    ranked = sorted(
        pooled,
        key=lambda g: (g.is_open_source_relevant, g.close_date or ""),
        reverse=True,
    )[:max_results]
    return json.dumps(
        {
            "focus": focus,
            "count": len(ranked),
            "open_source_bias": True,
            "opportunities": [_serialize(g) for g in ranked],
        },
        indent=2,
        default=str,
    )


@mcp.tool
async def list_public_goods_funding(max_results: int = 25) -> str:
    """List public-goods funding vehicles: sponsorships, collectives, quadratic rounds, open-source funds."""
    try:
        from opengos.sources.public_goods import list_catalog

        items = list_catalog()
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)
    return json.dumps(
        {
            "count": min(len(items), max_results),
            "items": items[:max_results],
            "notes": "Includes donations and sponsorship vehicles as first-class funding paths.",
        },
        indent=2,
        default=str,
    )


@mcp.tool
async def search_nsf_awards(keyword: str, max_results: int = 15) -> str:
    """Search NSF Awards API for research and cyberinfrastructure programs."""
    try:
        from opengos.sources.nsf import search_nsf

        results = await search_nsf(keyword=keyword, limit=max_results)
    except Exception as e:
        return json.dumps(
            {"error": str(e), "hint": "NSF public API may be temporarily unavailable"},
            indent=2,
        )
    return json.dumps(
        {"query": keyword, "count": len(results), "awards": results}, indent=2, default=str
    )


@mcp.tool
async def refresh_corpus() -> str:
    """Re-pull configured sources into the local corpus."""
    try:
        from opengos.ingestion.corpus import refresh

        stats = await refresh()
        return json.dumps({"status": "ok", "stats": stats}, indent=2, default=str)
    except Exception as e:
        return json.dumps({"status": "partial", "error": str(e)}, indent=2)


@mcp.tool
async def run_evaluation() -> str:
    """Run the discovery / open-source-relevance evaluation harness."""
    try:
        from opengos.evaluation.harness import run

        report = await run()
        return json.dumps(report, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool
async def upsert_profile(name: str, pitch: str = "", tags: str = "open-source") -> str:
    """Create or update the project profile used for ranking and grounded drafts."""
    try:
        from opengos.profile.steward import upsert

        profile = upsert(
            name=name,
            pitch=pitch,
            tags=[t.strip() for t in tags.split(",") if t.strip()],
        )
        return json.dumps({"status": "ok", "profile": profile}, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool
async def draft_proposal_outline(opportunity_id: str, project_name: str = "") -> str:
    """Build a grounded proposal outline for a grant or public-goods funding vehicle."""
    try:
        from opengos.drafting.drafter import outline

        draft = await outline(opportunity_id=opportunity_id, project_name=project_name or None)
        return json.dumps(draft, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.resource("opengos://status")
def status() -> str:
    return json.dumps(
        {
            "name": "OpenGOS",
            "version": "0.4.0",
            "transport": "stdio",
            "philosophy": "Public-good first. Strong provenance. Declared open-source ranking bias.",
        },
        indent=2,
    )


@mcp.resource("opengos://sources")
def data_sources() -> str:
    return json.dumps(
        {
            "primary": [
                {"name": "Grants.gov", "auth_required": False},
                {"name": "NSF Awards API", "auth_required": False},
            ],
            "public_goods": [
                "GitHub Sponsors",
                "Open Collective",
                "Gitcoin",
                "OpenSSF",
                "NumFOCUS",
                "PSF",
                "NLnet",
                "Sovereign Tech Agency",
            ],
        },
        indent=2,
    )


def main() -> None:
    logger.info("Starting OpenGOS MCP Server v0.4.0")
    mcp.run()


if __name__ == "__main__":
    main()
