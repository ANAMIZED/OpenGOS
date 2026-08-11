"""
Public Goods / Donation & Gifting funding sources.

This module surfaces non-traditional funding for open-source public goods:
GitHub Sponsors style programs, Open Collective, Gitcoin, foundation open-source funds,
and community donation opportunities. These are first-class citizens in OpenGrants OS
because many of the most important open-source AI contributions are funded this way.
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
    type: str  # "donation" | "sponsorship" | "quadratic" | "grant" | "bounty" | "collective"
    description: str | None = None
    url: str | None = None
    focus_areas: list[str] = Field(default_factory=list)
    open_source_preferred: bool = True
    retrieved_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    notes: str | None = None


class PublicGoodsFundingClient:
    """
    Curated + extensible catalog of public-goods / donation funding sources
    relevant to open-source AI and public-interest technology.
    """

    CATALOG: list[dict[str, Any]] = [
        {
            "id": "github-sponsors",
            "title": "GitHub Sponsors",
            "organization": "GitHub",
            "type": "sponsorship",
            "description": "Direct sponsorship of open-source maintainers and projects via GitHub.",
            "url": "https://github.com/sponsors",
            "focus_areas": ["open-source", "maintainers", "ai", "developer-tools"],
            "open_source_preferred": True,
            "notes": "Best for individual maintainers and small projects with existing GitHub presence.",
        },
        {
            "id": "open-collective",
            "title": "Open Collective",
            "organization": "Open Collective",
            "type": "collective",
            "description": "Transparent collectives for open-source projects and public-goods communities. Supports recurring donations and fiscal hosting.",
            "url": "https://opencollective.com",
            "focus_areas": ["open-source", "public-goods", "communities", "fiscal-hosting"],
            "open_source_preferred": True,
        },
        {
            "id": "gitcoin",
            "title": "Gitcoin Grants / Allo",
            "organization": "Gitcoin",
            "type": "quadratic",
            "description": "Quadratic funding rounds and Allo protocol for public goods, including open-source and public-interest technology.",
            "url": "https://gitcoin.co",
            "focus_areas": ["public-goods", "open-source", "web3", "climate", "ai-ethics"],
            "open_source_preferred": True,
            "notes": "Strong fit for public-goods AI and open-source infrastructure.",
        },
        {
            "id": "sentient-foundation",
            "title": "Sentient Foundation AGI Grants",
            "organization": "Sentient Foundation",
            "type": "grant",
            "description": "Grants focused on open AGI research and open-source AI systems.",
            "url": "https://sentient.foundation",
            "focus_areas": ["open-agi", "open-source-ai", "research"],
            "open_source_preferred": True,
        },
        {
            "id": "openssf",
            "title": "OpenSSF / Linux Foundation Security Grants",
            "organization": "Open Source Security Foundation (Linux Foundation)",
            "type": "grant",
            "description": "Funding for open-source security improvements, critical infrastructure, and secure software supply chain work.",
            "url": "https://openssf.org",
            "focus_areas": ["open-source-security", "supply-chain", "critical-infrastructure"],
            "open_source_preferred": True,
        },
        {
            "id": "numfocus",
            "title": "NumFOCUS Small Development Grants",
            "organization": "NumFOCUS",
            "type": "grant",
            "description": "Support for open-source scientific computing projects (many of which underpin AI research).",
            "url": "https://numfocus.org",
            "focus_areas": ["scientific-computing", "open-source", "data-science", "ai-tooling"],
            "open_source_preferred": True,
        },
        {
            "id": "psf",
            "title": "Python Software Foundation Grants",
            "organization": "Python Software Foundation",
            "type": "grant",
            "description": "Grants supporting the Python ecosystem, including AI/ML libraries and community work.",
            "url": "https://www.python.org/psf/grants/",
            "focus_areas": ["python", "open-source", "education", "community"],
            "open_source_preferred": True,
        },
        {
            "id": "mozilla-open-source",
            "title": "Mozilla Open Source Support (MOSS) / related programs",
            "organization": "Mozilla",
            "type": "grant",
            "description": "Historic and ongoing support for open-source projects aligned with open internet and public-interest technology.",
            "url": "https://www.mozilla.org",
            "focus_areas": ["open-source", "public-interest", "privacy", "open-web"],
            "open_source_preferred": True,
        },
    ]

    def list_opportunities(
        self,
        focus: str | None = None,
        type_filter: str | None = None,
    ) -> list[PublicGoodsOpportunity]:
        results = []
        for item in self.CATALOG:
            if type_filter and item["type"] != type_filter:
                continue
            if focus:
                text = f"{item['title']} {item.get('description','')} {' '.join(item.get('focus_areas', []))}".lower()
                if focus.lower() not in text:
                    continue
            results.append(PublicGoodsOpportunity(**item))
        return results

    def get_by_id(self, opportunity_id: str) -> PublicGoodsOpportunity | None:
        for item in self.CATALOG:
            if item["id"] == opportunity_id:
                return PublicGoodsOpportunity(**item)
        return None
