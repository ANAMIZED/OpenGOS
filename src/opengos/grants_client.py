"""
Grants data access layer with strong provenance and multi-source readiness.

Currently powered primarily by the public Grants.gov search2 API.
Designed for easy extension to NSF, NIH, Horizon Europe, foundations, etc.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

import httpx
from pydantic import BaseModel, Field

logger = logging.getLogger("opengos.grants_client")

GRANTS_GOV_SEARCH_URL = "https://api.grants.gov/v1/api/search2"


class GrantOpportunity(BaseModel):
    """Normalized grant opportunity with full provenance."""

    id: str
    title: str
    agency: str | None = None
    open_date: str | None = None
    close_date: str | None = None
    opportunity_number: str | None = None
    cfda_list: list[str] = Field(default_factory=list)
    award_ceiling: float | None = None
    award_floor: float | None = None
    description: str | None = None
    eligibility: str | None = None
    funding_instrument: str | None = None
    category: str | None = None
    source_url: str | None = None
    source: str = "grants.gov"
    retrieved_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    raw: dict[str, Any] = Field(default_factory=dict, repr=False)

    @property
    def is_open_source_relevant(self) -> bool:
        text = f"{self.title} {self.description or ''}".lower()
        signals = [
            "open source",
            "opensource",
            "open-source",
            "open weight",
            "open model",
            "public interest technology",
            "open science",
            "reproducible",
            "open data",
        ]
        return any(s in text for s in signals)


class GrantsClient:
    """Async client for grant opportunity sources."""

    def __init__(self, timeout: float = 30.0, user_agent: str = "OpenGOS/0.4"):
        self.timeout = timeout
        self.user_agent = user_agent
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                follow_redirects=True,
                headers={"User-Agent": self.user_agent},
            )
        return self._client

    async def aclose(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    async def search(
        self,
        keyword: str | None = None,
        rows: int = 25,
        start_record: int = 0,
        opp_statuses: str = "posted",
    ) -> list[GrantOpportunity]:
        """Search the public Grants.gov API. No API key required."""
        payload: dict[str, Any] = {
            "rows": min(max(rows, 1), 100),
            "startRecordNum": max(start_record, 0),
            "oppStatuses": opp_statuses,
        }
        if keyword and keyword.strip():
            payload["keyword"] = keyword.strip()

        client = await self._get_client()
        try:
            resp = await client.post(
                GRANTS_GOV_SEARCH_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPStatusError as e:
            logger.error("Grants.gov HTTP error %s: %s", e.response.status_code, e)
            return []
        except Exception as e:
            logger.exception("Grants.gov search failed: %s", e)
            return []

        opportunities: list[GrantOpportunity] = []
        hits = (
            data.get("data")
            or data.get("oppHits")
            or data.get("opportunities")
            or []
        )
        if isinstance(hits, dict):
            hits = hits.get("oppHits") or hits.get("results") or []

        for item in hits or []:
            try:
                opp = self._normalize(item)
                if opp:
                    opportunities.append(opp)
            except Exception as e:
                logger.warning("Failed to normalize opportunity item: %s", e)
                continue

        return opportunities

    def _normalize(self, item: dict[str, Any]) -> GrantOpportunity | None:
        opp_id = str(
            item.get("id")
            or item.get("opportunityId")
            or item.get("oppId")
            or item.get("number")
            or ""
        ).strip()
        if not opp_id:
            return None

        title = (
            item.get("title")
            or item.get("opportunityTitle")
            or item.get("oppTitle")
            or "Untitled Opportunity"
        )
        agency = (
            item.get("agency")
            or item.get("agencyName")
            or item.get("owningAgencyCode")
            or item.get("agencyCode")
        )
        close_date = (
            item.get("closeDate")
            or item.get("closingDate")
            or item.get("oppCloseDate")
            or item.get("closeDateStr")
        )
        open_date = item.get("openDate") or item.get("openingDate") or item.get("postDate")
        number = item.get("number") or item.get("opportunityNumber") or item.get("oppNumber")
        description = (
            item.get("description")
            or item.get("synopsis")
            or item.get("synopsisDesc")
            or item.get("abstract")
        )
        source_url = f"https://www.grants.gov/search-results-detail/{opp_id}"

        return GrantOpportunity(
            id=opp_id,
            title=str(title).strip(),
            agency=str(agency).strip() if agency else None,
            open_date=str(open_date) if open_date else None,
            close_date=str(close_date) if close_date else None,
            opportunity_number=str(number) if number else None,
            description=str(description).strip() if description else None,
            source_url=source_url,
            source="grants.gov",
            raw=item,
        )


_client: GrantsClient | None = None


async def get_client() -> GrantsClient:
    global _client
    if _client is None:
        _client = GrantsClient()
    return _client
