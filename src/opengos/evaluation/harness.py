"""
Lightweight evaluation harness.

Measures basic discovery quality and open-source relevance signal.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from opengos.grants_client import get_client

logger = logging.getLogger("opengos.evaluation")


async def run_basic_evaluation(queries: list[str] | None = None) -> dict[str, Any]:
    queries = queries or [
        "open source artificial intelligence",
        "machine learning research",
        "open science",
        "public interest technology",
    ]

    client = await get_client()
    results_summary = []
    total_opps = 0
    total_os_relevant = 0

    for q in queries:
        opps = await client.search(keyword=q, rows=10)
        os_count = sum(1 for o in opps if o.is_open_source_relevant)
        total_opps += len(opps)
        total_os_relevant += os_count
        results_summary.append(
            {
                "query": q,
                "returned": len(opps),
                "open_source_relevant": os_count,
            }
        )

    return {
        "queries_evaluated": len(queries),
        "total_opportunities_retrieved": total_opps,
        "total_open_source_relevant": total_os_relevant,
        "open_source_hit_rate": round(total_os_relevant / max(total_opps, 1), 3),
        "per_query": results_summary,
        "notes": (
            "Basic discovery health check. Future harness will include "
            "ranking quality, citation grounding rate, and human preference data."
        ),
    }


async def run() -> dict[str, Any]:
    """MCP-facing alias for the evaluation harness."""
    return await run_basic_evaluation()


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    result = asyncio.run(run_basic_evaluation())
    import json

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
