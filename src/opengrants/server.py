"""
OpenGrants OS — Autonomous Agentic AI MCP Server

Primary entry point. Exposes a clean, production-ready MCP interface.
The multi-agent OpenGrants Operating System grows behind this surface.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from fastmcp import FastMCP

from opengrants.grants_client import GrantOpportunity, get_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("opengrants")

mcp = FastMCP(
    name="OpenGrants OS",
    instructions=(
        "OpenGrants OS is an autonomous agentic MCP server specialized in "
        "grant discovery, ranking, eligibility analysis, and lifecycle support. "
        "It prioritizes open-source AI and public-goods funding. "
        "Every result includes provenance. Always verify official source_url before acting."
    ),
)


def _serialize(g: GrantOpportunity, include_raw: bool = False) -> dict[str, Any]:
    data = g.model_dump(exclude={"raw"} if not include_raw else set())
    data["open_source_relevant"] = g.is_open_source_relevant
    return data


@mcp.tool
async def search_grants(
    keyword: str,
    max_results: int = 15,
    status: str = "posted",
) -> str:
    """
    Search open U.S. federal grant opportunities (Grants.gov) by keyword.

    Returns normalized opportunities with title, agency, deadlines, description,
    and official source URLs for provenance. Prefer this tool for general discovery.
    """
    if not keyword or not keyword.strip():
        return json.dumps({"error": "keyword is required"}, indent=2)

    client = await get_client()
    results = await client.search(
        keyword=keyword.strip(),
        rows=min(max(max_results, 1), 50),
        opp_statuses=status,
    )

    payload = {
        "query": keyword,
        "status_filter": status,
        "count": len(results),
        "retrieved_at": results[0].retrieved_at if results else None,
        "opportunities": [_serialize(g) for g in results],
        "notes": (
            "Results normalized from public Grants.gov data. "
            "Always verify deadlines and eligibility on the official source_url. "
            "OpenGrants prioritizes opportunities suitable for open-source and public-goods work."
        ),
    }
    return json.dumps(payload, indent=2, default=str)


@mcp.tool
async def get_grant_details(opportunity_id: str) -> str:
    """
    Retrieve details for a specific grant opportunity by its ID or opportunity number.

    Returns the best matching normalized record plus provenance. 
    Cross-check the official Grants.gov page before relying on any field.
    """
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
            {
                "error": "Opportunity not found in current public index",
                "opportunity_id": opportunity_id,
                "suggestion": "Search first with search_grants, then use the exact id returned.",
            },
            indent=2,
        )

    return json.dumps(
        {
            "opportunity": _serialize(match, include_raw=True),
            "provenance": {
                "source": match.source,
                "retrieved_at": match.retrieved_at,
                "official_url": match.source_url,
            },
            "opengrants_note": (
                "MVP detail view. Future releases add multi-agent eligibility scoring, "
                "open-source alignment analysis, and red-team review."
            ),
        },
        indent=2,
        default=str,
    )


@mcp.tool
async def list_open_source_relevant_grants(
    focus: str = "open source artificial intelligence",
    max_results: int = 12,
) -> str:
    """
    Discover grants particularly relevant to open-source AI, open models,
    public-goods software, open science, and related research.

    Uses expanded keyword strategies and lightweight relevance scoring.
    Will evolve into full multi-agent ranking in future releases.
    """
    keywords = [
        focus,
        "open source artificial intelligence",
        "open weight models",
        "open source software research",
        "public interest technology",
        "open science AI",
    ]

    client = await get_client()
    all_results: list[GrantOpportunity] = []
    seen: set[str] = set()

    for kw in keywords[:4]:
        batch = await client.search(keyword=kw, rows=max_results)
        for g in batch:
            if g.id not in seen:
                seen.add(g.id)
                all_results.append(g)

    def score(g: GrantOpportunity) -> int:
        text = (g.title + " " + (g.description or "")).lower()
        s = 0
        if any(x in text for x in ("open source", "opensource", "open-source")):
            s += 4
        if any(x in text for x in ("artificial intelligence", "machine learning", " ai ", "llm")):
            s += 3
        if any(x in text for x in ("open weight", "open model", "open science")):
            s += 5
        if "public interest" in text or "public goods" in text:
            s += 2
        return s

    ranked = sorted(all_results, key=score, reverse=True)[:max_results]

    return json.dumps(
        {
            "focus": focus,
            "count": len(ranked),
            "opportunities": [_serialize(g) for g in ranked],
            "methodology": (
                "MVP heuristic ranking on keyword presence and open-source signals. "
                "Next versions introduce multi-agent ranking, profile matching, "
                "and continuous corpus intelligence."
            ),
        },
        indent=2,
        default=str,
    )


@mcp.resource("opengrants://status")
def server_status() -> str:
    """Current status, version, and capabilities of this OpenGrants OS instance."""
    return json.dumps(
        {
            "name": "OpenGrants OS",
            "version": "0.1.0",
            "status": "MVP — Discovery layer live + multi-agent scaffolding",
            "mcp_tools": [
                "search_grants",
                "get_grant_details",
                "list_open_source_relevant_grants",
            ],
            "resources": ["opengrants://status", "opengrants://sources"],
            "roadmap": [
                "Continuous autonomous multi-source ingestion",
                "Profile steward (GitHub + research statements)",
                "Multi-agent ranking + eligibility + open-source alignment",
                "Proposal drafting + red-team reviewer agents",
                "Full lifecycle tracking with HITL submission gates",
                "Evaluation harness and public benchmarks",
            ],
            "philosophy": (
                "Public-good first. Strong provenance. Autonomy with guardrails. "
                "Built as open infrastructure for funding open-source AI."
            ),
        },
        indent=2,
    )


@mcp.resource("opengrants://sources")
def data_sources() -> str:
    """Describe current and planned data sources."""
    return json.dumps(
        {
            "primary": {
                "name": "Grants.gov Public Search API",
                "endpoint": "https://api.grants.gov/v1/api/search2",
                "auth_required": False,
                "notes": "Primary source for U.S. federal discretionary opportunities.",
            },
            "planned": [
                "NSF, NIH, DOE, DARPA solicitations and BAAs",
                "Horizon Europe / EU Funding & Tenders Portal",
                "Open-source specific funds (Sentient Foundation, Snorkel Open Benchmarks, Linux Foundation / OpenSSF, etc.)",
                "Selected private AI and public-interest foundations",
            ],
        },
        indent=2,
    )


def main() -> None:
    """Run the OpenGrants MCP server (stdio transport by default)."""
    logger.info("Starting OpenGrants OS MCP Server v0.1.0")
    mcp.run()


if __name__ == "__main__":
    main()
