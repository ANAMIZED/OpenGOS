"""
OpenGrants OS — Autonomous Agentic AI MCP Server v0.2.0

Primary entry point. Exposes a clean, production-ready MCP interface.
Includes traditional grants, public-goods/donation sources, profile steward,
and drafting agents.
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
        "grant discovery, ranking, eligibility analysis, drafting, and lifecycle support. "
        "It prioritizes open-source AI and public-goods funding, including donations, "
        "sponsorships, and quadratic funding vehicles. Every result includes provenance."
    ),
)


def _serialize(g: GrantOpportunity, include_raw: bool = False) -> dict[str, Any]:
    data = g.model_dump(exclude={"raw"} if not include_raw else set())
    data["open_source_relevant"] = g.is_open_source_relevant
    return data


@mcp.tool
async def search_grants(keyword: str, max_results: int = 15, status: str = "posted") -> str:
    """Search open U.S. federal grant opportunities (Grants.gov) by keyword with provenance."""
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


@mcp.tool
async def get_grant_details(opportunity_id: str) -> str:
    """Retrieve details for a specific grant opportunity by ID."""
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


@mcp.tool
async def list_open_source_relevant_grants(focus: str = "open source artificial intelligence", max_results: int = 12) -> str:
    """Discover grants particularly relevant to open-source AI and public goods."""
    keywords = [focus, "open source artificial intelligence", "open weight models", "public interest technology"]
    client = await get_client()
    all_results: list[GrantOpportunity] = []
    seen: set[str] = set()
    for kw in keywords[:3]:
        batch = await client.search(keyword=kw, rows=max_results)
        for g in batch:
            if g.id not in seen:
                seen.add(g.id)
                all_results.append(g)
    def score(g: GrantOpportunity) -> int:
        text = (g.title + " " + (g.description or "")).lower()
        s = 0
        if any(x in text for x in ("open source", "opensource", "open-source")): s += 4
        if any(x in text for x in ("artificial intelligence", "machine learning", " ai ", "llm")): s += 3
        if any(x in text for x in ("open weight", "open model", "open science")): s += 5
        return s
    ranked = sorted(all_results, key=score, reverse=True)[:max_results]
    return json.dumps({"focus": focus, "count": len(ranked), "opportunities": [_serialize(g) for g in ranked]}, indent=2, default=str)


@mcp.tool
async def list_public_goods_funding(focus: str = "open source", type_filter: str = "") -> str:
    """List donation, sponsorship, quadratic funding, and open-source public-goods funding opportunities (GitHub Sponsors, Open Collective, Gitcoin, Sentient, OpenSSF, NumFOCUS, PSF, etc.)."""
    from opengrants.sources.public_goods import PublicGoodsFundingClient
    client = PublicGoodsFundingClient()
    results = client.list_opportunities(focus=focus if focus else None, type_filter=type_filter if type_filter else None)
    return json.dumps({"count": len(results), "opportunities": [r.model_dump() for r in results], "note": "Curated high-signal public-goods funding sources. Community PRs welcome."}, indent=2, default=str)


@mcp.tool
async def search_nsf_awards(keyword: str, max_results: int = 15) -> str:
    """Search NSF Awards (public API) for historical and active awards."""
    from opengrants.sources.nsf import NSFClient
    client = NSFClient()
    awards = await client.search(keyword=keyword, rows=max_results)
    return json.dumps({"query": keyword, "count": len(awards), "awards": [a.model_dump(exclude={"raw"}) for a in awards]}, indent=2, default=str)


@mcp.tool
async def refresh_corpus(keywords: str = "artificial intelligence,open source,machine learning") -> str:
    """Trigger continuous-ingestion style refresh of the local grant corpus."""
    from opengrants.ingestion.corpus import CorpusManager
    mgr = CorpusManager()
    kws = [k.strip() for k in keywords.split(",") if k.strip()]
    added = await mgr.refresh(keywords=kws)
    return json.dumps({"added": added, "corpus_stats": mgr.stats()}, indent=2)


@mcp.tool
async def run_evaluation() -> str:
    """Run the basic OpenGrants evaluation harness."""
    from opengrants.evaluation.harness import run_basic_evaluation
    result = await run_basic_evaluation()
    return json.dumps(result, indent=2)


@mcp.tool
async def upsert_profile(profile_id: str, name: str, description: str, github_url: str = "", focus_areas: str = "") -> str:
    """Create or update a project/researcher profile for matching and drafting. focus_areas = comma-separated."""
    from opengrants.profile.steward import ProfileSteward
    steward = ProfileSteward()
    areas = [a.strip() for a in focus_areas.split(",") if a.strip()] if focus_areas else []
    profile = steward.from_text(profile_id=profile_id, name=name, description=description, github_url=github_url or None, focus_areas=areas)
    return json.dumps(profile.model_dump(), indent=2, default=str)


@mcp.tool
async def draft_proposal_outline(profile_id: str, opportunity_title: str, opportunity_description: str = "", opportunity_type: str = "grant") -> str:
    """Generate a grounded proposal outline + short pitch for a profile + opportunity (works for grants and donation/public-goods vehicles)."""
    from opengrants.profile.steward import ProfileSteward, ProjectProfile
    from opengrants.drafting.drafter import ProposalDrafter
    steward = ProfileSteward()
    profile = steward.get(profile_id)
    if not profile:
        profile = ProjectProfile(id=profile_id, name=profile_id, description="Open-source AI project")
        steward.upsert(profile)
    drafter = ProposalDrafter()
    outline = drafter.draft_outline(profile=profile, opportunity_title=opportunity_title, opportunity_description=opportunity_description or None, opportunity_type=opportunity_type)
    outline["short_pitch"] = drafter.draft_short_pitch(profile, opportunity_title)
    return json.dumps(outline, indent=2, default=str)


@mcp.resource("opengrants://status")
def server_status() -> str:
    return json.dumps({
        "name": "OpenGrants OS",
        "version": "0.2.0",
        "status": "Public-goods + grants + profile + drafting live",
        "mcp_tools": ["search_grants", "get_grant_details", "list_open_source_relevant_grants", "list_public_goods_funding", "search_nsf_awards", "refresh_corpus", "run_evaluation", "upsert_profile", "draft_proposal_outline"],
        "resources": ["opengrants://status", "opengrants://sources"],
        "philosophy": "Public-good first. Strong provenance. Autonomy with guardrails. Includes donation/gifting sources as first-class citizens.",
    }, indent=2)


@mcp.resource("opengrants://sources")
def data_sources() -> str:
    return json.dumps({
        "primary": [{"name": "Grants.gov", "auth_required": False}, {"name": "NSF Awards API", "auth_required": False}],
        "public_goods": ["GitHub Sponsors", "Open Collective", "Gitcoin", "Sentient Foundation", "OpenSSF", "NumFOCUS", "PSF", "Mozilla"],
        "planned": ["NIH", "Horizon Europe", "additional foundation open-source programs"],
    }, indent=2)


def main() -> None:
    logger.info("Starting OpenGrants OS MCP Server v0.2.0")
    mcp.run()


if __name__ == "__main__":
    main()
