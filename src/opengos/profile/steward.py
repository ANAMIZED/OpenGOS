"""
Profile Steward

Maintains structured profiles of researchers, open-source projects, and organizations
so that ranking, eligibility, and drafting can be personalized.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class ProjectProfile(BaseModel):
    """A project or personal research/open-source profile."""

    id: str
    name: str
    description: str | None = None
    github_url: str | None = None
    website: str | None = None
    focus_areas: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    past_grants: list[str] = Field(default_factory=list)
    open_source_license: str | None = None
    primary_language: str | None = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    extra: dict[str, Any] = Field(default_factory=dict)


class ProfileSteward:
    """Simple in-memory profile store (replace with DB in production)."""

    def __init__(self) -> None:
        self._profiles: dict[str, ProjectProfile] = {}

    def upsert(self, profile: ProjectProfile) -> ProjectProfile:
        profile.updated_at = datetime.now(timezone.utc).isoformat()
        self._profiles[profile.id] = profile
        return profile

    def get(self, profile_id: str) -> ProjectProfile | None:
        return self._profiles.get(profile_id)

    def list_profiles(self) -> list[ProjectProfile]:
        return list(self._profiles.values())

    def delete(self, profile_id: str) -> bool:
        if profile_id in self._profiles:
            del self._profiles[profile_id]
            return True
        return False

    def from_text(
        self,
        profile_id: str,
        name: str,
        description: str,
        github_url: str | None = None,
        focus_areas: list[str] | None = None,
    ) -> ProjectProfile:
        profile = ProjectProfile(
            id=profile_id,
            name=name,
            description=description,
            github_url=github_url,
            focus_areas=focus_areas or [],
            keywords=self._extract_keywords(description),
        )
        return self.upsert(profile)

    def _extract_keywords(self, text: str) -> list[str]:
        candidates = [
            "open source",
            "artificial intelligence",
            "machine learning",
            "llm",
            "open weight",
            "public goods",
            "reproducibility",
            "open science",
            "security",
            "privacy",
            "climate",
            "education",
            "healthcare",
        ]
        text_l = text.lower()
        return [c for c in candidates if c in text_l]


_steward: ProfileSteward | None = None


def get_steward() -> ProfileSteward:
    global _steward
    if _steward is None:
        _steward = ProfileSteward()
    return _steward


def _slug(name: str) -> str:
    return name.lower().replace(" ", "-")


def upsert(name: str, pitch: str = "", tags: list[str] | None = None) -> dict[str, Any]:
    """MCP-facing profile upsert helper."""
    steward = get_steward()
    profile = steward.from_text(
        profile_id=_slug(name),
        name=name,
        description=pitch or name,
        focus_areas=tags or ["open-source"],
    )
    return profile.model_dump()


def get_profile(name: str) -> dict[str, Any]:
    steward = get_steward()
    profile = steward.get(_slug(name)) or steward.get(name)
    if profile is None:
        return {"error": f"profile not found: {name}"}
    return profile.model_dump()


def list_profiles() -> list[dict[str, Any]]:
    return [p.model_dump() for p in get_steward().list_profiles()]


def delete_profile(name: str) -> dict[str, Any]:
    steward = get_steward()
    for key in (_slug(name), name):
        if steward.delete(key):
            return {"status": "deleted", "id": key}
    return {"error": f"profile not found: {name}"}
