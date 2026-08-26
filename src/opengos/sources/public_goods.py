"""
Public Goods / Donation & Gifting funding sources.

Surfaces non-traditional funding for open-source public goods:
GitHub Sponsors, Open Collective, Gitcoin, foundation open-source funds,
and community donation vehicles. First-class citizens in OpenGOS.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class PublicGoodsOpportunity(BaseModel):
    """A donation, sponsorship, or public-goods funding opportunity."""

    id: str
    title: str
    organization: str
    type: str
    description: str | None = None
    url: str | None = None
    focus_areas: list[str] = Field(default_factory=list)
    open_source_preferred: bool = True
    retrieved_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    notes: str | None = None


class PublicGoodsFundingClient:
    """Curated catalog of public-goods / donation funding sources."""

    CATALOG: list[dict[str, Any]] = [
        {
            "id": "pg-github-sponsors",
            "title": "GitHub Sponsors",
            "organization": "GitHub",
            "type": "sponsorship",
            "description": "Recurring and one-time sponsorships to maintainers and organizations.",
            "url": "https://github.com/sponsors",
            "focus_areas": ["open-source", "maintainers", "community"],
            "open_source_preferred": True,
            "notes": "Enable Sponsors on the account or org; FUNDING.yml surfaces the button.",
        },
        {
            "id": "pg-open-collective",
            "title": "Open Collective / Open Source Collective",
            "organization": "Open Collective",
            "type": "collective",
            "description": "Transparent fiscal hosting so projects can accept donations and pay contributors.",
            "url": "https://opencollective.com",
            "focus_areas": ["open-source", "community", "fiscal-host"],
            "open_source_preferred": True,
            "notes": "Prefer OSC or another active fiscal host; set open_collective slug in FUNDING.yml.",
        },
        {
            "id": "pg-gitcoin",
            "title": "Gitcoin Grants",
            "organization": "Gitcoin",
            "type": "quadratic",
            "description": "Quadratic and multi-mechanism funding rounds for public goods.",
            "url": "https://www.gitcoin.co",
            "focus_areas": ["open-source", "web3", "public-goods"],
            "open_source_preferred": True,
        },
        {
            "id": "pg-nlnet",
            "title": "NLnet / Open Internet programmes",
            "organization": "NLnet Foundation",
            "type": "grant",
            "description": "Small-to-medium grants for open internet and digital commons technology.",
            "url": "https://nlnet.nl/propose/",
            "focus_areas": ["open-source", "internet", "privacy", "commons"],
            "open_source_preferred": True,
            "notes": "Call windows change; verify open topics on nlnet.nl.",
        },
        {
            "id": "pg-sovereign-tech",
            "title": "Sovereign Tech Agency Fund",
            "organization": "Sovereign Tech Agency",
            "type": "grant",
            "description": "Investment in critical open-source infrastructure and resilience.",
            "url": "https://www.sovereign.tech/",
            "focus_areas": ["open-source", "infrastructure", "security"],
            "open_source_preferred": True,
        },
        {
            "id": "pg-prototype-fund",
            "title": "Prototype Fund",
            "organization": "Prototype Fund / BMBF",
            "type": "grant",
            "description": "Public-interest tech prototypes released as open source (Germany-focused).",
            "url": "https://prototypefund.de",
            "focus_areas": ["open-source", "public-interest", "security"],
            "open_source_preferred": True,
        },
        {
            "id": "pg-openssf",
            "title": "OpenSSF / Alpha-Omega",
            "organization": "Open Source Security Foundation",
            "type": "grant",
            "description": "Security investment and engagements for critical open-source projects.",
            "url": "https://openssf.org/",
            "focus_areas": ["open-source", "security", "infrastructure"],
            "open_source_preferred": True,
            "notes": "Often proactive/invited; still relevant for critical projects.",
        },
        {
            "id": "pg-numfocus",
            "title": "NumFOCUS Small Development Grants",
            "organization": "NumFOCUS",
            "type": "grant",
            "description": "Small grants for open-source scientific computing projects.",
            "url": "https://numfocus.org/",
            "focus_areas": ["open-source", "science", "python"],
            "open_source_preferred": True,
        },
        {
            "id": "pg-psf",
            "title": "Python Software Foundation Grants",
            "organization": "Python Software Foundation",
            "type": "grant",
            "description": "Support for Python community and open-source initiatives.",
            "url": "https://www.python.org/psf/grants/",
            "focus_areas": ["open-source", "python", "community"],
            "open_source_preferred": True,
            "notes": "Program scope and windows vary by year; verify current call.",
        },
    ]

    def list_all(self) -> list[PublicGoodsOpportunity]:
        now = datetime.now(timezone.utc).isoformat()
        out: list[PublicGoodsOpportunity] = []
        for item in self.CATALOG:
            out.append(
                PublicGoodsOpportunity(
                    id=item["id"],
                    title=item["title"],
                    organization=item["organization"],
                    type=item["type"],
                    description=item.get("description"),
                    url=item.get("url"),
                    focus_areas=list(item.get("focus_areas") or []),
                    open_source_preferred=bool(item.get("open_source_preferred", True)),
                    retrieved_at=now,
                    notes=item.get("notes"),
                )
            )
        return out


def list_catalog() -> list[dict[str, Any]]:
    """Return serializable public-goods catalog for MCP tools."""
    client = PublicGoodsFundingClient()
    return [o.model_dump() for o in client.list_all()]


def get_item(item_id: str) -> dict[str, Any] | None:
    """Lookup one catalog entry by id or title substring."""
    needle = (item_id or "").strip().lower()
    if not needle:
        return None
    for item in list_catalog():
        title = str(item.get("title") or "").lower()
        if item.get("id") == item_id or needle in title or needle == str(item.get("id") or "").lower():
            return item
    return None
