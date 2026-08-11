"""
LangGraph orchestration scaffold for OpenGrants OS.

This module defines the high-level multi-agent graph that will power
autonomous discovery, ranking, drafting, and lifecycle management.

Currently a clean scaffold so the system can grow without breaking the
MCP surface.
"""

from __future__ import annotations

from typing import Any, TypedDict

# Soft imports so the core MCP server works even without agents extras installed
try:
    from langgraph.graph import StateGraph, END, START
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    StateGraph = None  # type: ignore
    END = START = None  # type: ignore


class OpenGrantsState(TypedDict, total=False):
    """Shared state for the OpenGrants multi-agent system."""
    query: str
    profile: dict[str, Any]
    opportunities: list[dict[str, Any]]
    ranked: list[dict[str, Any]]
    draft: str | None
    red_team_feedback: str | None
    messages: list[Any]
    next_action: str


def create_opengrants_graph():
    """
    Create the core OpenGrants LangGraph.

    Nodes (planned / partial):
    - discovery
    - ranking
    - eligibility
    - drafting
    - red_team
    - human_approval

    Returns a compiled graph when langgraph is installed, otherwise None.
    """
    if not LANGGRAPH_AVAILABLE:
        return None

    graph = StateGraph(OpenGrantsState)

    # Placeholder nodes — real agent logic lands here in subsequent iterations
    def discovery_node(state: OpenGrantsState) -> dict:
        return {"next_action": "ranking", "opportunities": state.get("opportunities", [])}

    def ranking_node(state: OpenGrantsState) -> dict:
        return {"next_action": "eligibility", "ranked": state.get("opportunities", [])}

    def eligibility_node(state: OpenGrantsState) -> dict:
        return {"next_action": "end"}

    graph.add_node("discovery", discovery_node)
    graph.add_node("ranking", ranking_node)
    graph.add_node("eligibility", eligibility_node)

    graph.add_edge(START, "discovery")
    graph.add_edge("discovery", "ranking")
    graph.add_edge("ranking", "eligibility")
    graph.add_edge("eligibility", END)

    return graph.compile()
