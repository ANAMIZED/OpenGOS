"""NSF Awards API client (public data)."""

from __future__ import annotations

import logging
from typing import Any

import httpx
from pydantic import BaseModel, Field

logger = logging.getLogger("opengos.sources.nsf")


class NSFAward(BaseModel):
    id: str
    title: str
    agency: str = "NSF"
    abstract: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    amount: float | None = None
    pi: str | None = None
    organization: str | None = None
    source_url: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict, repr=False)


class NSFClient:
    """Lightweight client for NSF Awards Search (public)."""

    BASE = "https://api.nsf.gov/services/v1/awards.json"

    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout

    async def search(self, keyword: str, rows: int = 25) -> list[NSFAward]:
        params = {
            "keyword": keyword,
            "printFields": (
                "id,title,abstractText,startDate,expDate,"
                "estimatedTotalAmt,piFirstName,piLastName,awardeeName"
            ),
            "rpp": min(rows, 100),
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(self.BASE, params=params)
                resp.raise_for_status()
                data = resp.json()
        except Exception as e:
            logger.exception("NSF search failed: %s", e)
            return []

        awards = []
        response = data.get("response", {})
        for item in response.get("award", []) or []:
            try:
                award_id = str(item.get("id", ""))
                awards.append(
                    NSFAward(
                        id=award_id,
                        title=item.get("title") or "Untitled",
                        abstract=item.get("abstractText"),
                        start_date=item.get("startDate"),
                        end_date=item.get("expDate"),
                        amount=(
                            float(item["estimatedTotalAmt"])
                            if item.get("estimatedTotalAmt")
                            else None
                        ),
                        pi=(
                            f"{item.get('piFirstName', '')} {item.get('piLastName', '')}".strip()
                            or None
                        ),
                        organization=item.get("awardeeName"),
                        source_url=(
                            f"https://www.nsf.gov/awardsearch/showAward?AWD_ID={award_id}"
                            if award_id
                            else None
                        ),
                        raw=item,
                    )
                )
            except Exception:
                continue
        return awards


async def search_nsf(keyword: str, limit: int = 15) -> list[dict[str, Any]]:
    """MCP-facing NSF search helper."""
    client = NSFClient()
    awards = await client.search(keyword=keyword, rows=limit)
    return [a.model_dump(exclude={"raw"}) for a in awards]
