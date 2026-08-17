"""OpenGOS Python SDK."""
from __future__ import annotations

from typing import Any, Optional

import httpx


class OpenGOSClient:
    def __init__(self, base_url: str = "http://localhost:8080", timeout: float = 60.0) -> None:
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(base_url=self.base_url, timeout=timeout)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "OpenGOSClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def health(self) -> dict[str, Any]:
        r = self._client.get("/health")
        r.raise_for_status()
        return r.json()

    def search_grants(self, query: str, limit: int = 10) -> dict[str, Any]:
        r = self._client.get("/v1/grants/search", params={"q": query, "limit": limit})
        r.raise_for_status()
        return r.json()

    def draft_proposal(self, opportunity_id: str, profile: Optional[dict] = None) -> dict[str, Any]:
        r = self._client.post(
            "/v1/proposals/draft",
            json={"opportunity_id": opportunity_id, "profile": profile or {}},
        )
        r.raise_for_status()
        return r.json()
