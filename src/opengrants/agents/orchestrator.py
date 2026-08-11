"""
LangGraph orchestration for OpenGrants OS.

Provides a real (if still lightweight) multi-agent flow:
discovery → ranking (with open-source bias) → eligibility scaffolding.
"""

from __future__ import annotations

import logging
from typing import Any, TypedDict

logger = logging.getLogger("opengrants.agents")

try:
    from langgraph.graph import StateGraph, END, START
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    StateGraph = END = START = None  # type: ignore


class OpenGrantsState(TypedDict, total=False):
    query: str
    profile: dict[str, Any]
    opportunities: list[dict[str, Any]]
    ranked: list[dict[str, Any]]
    draft: str | None
    red_team_feedback: str | None
    messages: list[Any]
    next_action: str
    error: str | None


def _score_open_source(opp: dict[str, Any]) -> int:
    text = f"{opp.get('title', '')} {opp.get('description', '')}".lower()
    score = 0
    if any(x in text for x in ("open source", "opensource", "open-source")):
        score += 5
    if any(x in text for x in ("open weight", "open model", "open science")):
        score += 4
    if any(x in text for x in ("artificial intelligence", "machine learning", "llm", " ai ")):
        score += 3
    if "public interest" in text or "public goods" in text:
        score += 2
    if opp.get("open_source_relevant"):
        score += 3
    return score


async def discovery_node(state: OpenGrantsState) -> dict:
    """Fetch opportunities for the current query."""
    from opengrants.grants_client import get_client

    query = state.get("query") or "open source artificial intelligence"
    client = await get_client()
    results = await client.search(keyword=query, rows=20)
    opps = [r.model_dump(exclude={"raw"}) for r in results]
    for o in opps:
        o["open_source_relevant"] = any(
            s in f"{o.get('title','')} {o.get('description','')}".lower()
            for s in ("open source", "opensource", "open weight", "open model")
        )
    return {"opportunities": opps, "next_action": "ranking"}


def ranking_node(state: OpenGrantsState) -> dict:
    """Rank by open-source + AI relevance."""
    opps = state.get("opportunities") or []
    ranked = sorted(opps, key=_score_open_source, reverse=True)
    return {"ranked": ranked[:15], "next_action": "eligibility"}


def eligibility_node(state: OpenGrantsState) -> dict:
    """Placeholder for future hard eligibility rules + profile matching."""
    ranked = state.get("ranked") or []
    return {"ranked": ranked, "next_action": "end"}


def create_opengrants_graph():
    """Compile the OpenGrants multi-agent graph."""
    if not LANGGRAPH_AVAILABLE:
        logger.warning("langgraph not installed — returning None")
        return None

    graph = StateGraph(OpenGrantsState)

    graph.add_node("discovery", discovery_node)
    graph.add_node("ranking", ranking_node)
    graph.add_node("eligibility", eligibility_node)

    graph.add_edge(START, "discovery")
    graph.add_edge("discovery", "ranking")
    graph.add_edge("ranking", "eligibility")
    graph.add_edge("eligibility", END)

    return graph.compile()
