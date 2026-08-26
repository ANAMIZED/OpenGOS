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
