"""
Simple in-memory + file-backed corpus manager for continuous ingestion.

In production this would use Postgres + vector store + scheduled crawlers.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from opengrants.grants_client import GrantOpportunity, get_client

logger = logging.getLogger("opengrants.ingestion")


class CorpusManager:
    """Manages a local cache of grant opportunities and supports refresh."""

    def __init__(self, data_dir: str | Path = "data/corpus"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.data_dir / "index.jsonl"
        self._cache: dict[str, dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        if not self.index_path.exists():
            return
        with self.index_path.open() as f:
            for line in f:
                try:
                    item = json.loads(line)
                    self._cache[item["id"]] = item
                except Exception:
                    continue
        logger.info("Loaded %d opportunities from corpus", len(self._cache))

    def _persist(self, opp: GrantOpportunity) -> None:
        record = opp.model_dump(exclude={"raw"})
        record["open_source_relevant"] = opp.is_open_source_relevant
        self._cache[opp.id] = record
        with self.index_path.open("a") as f:
            f.write(json.dumps(record, default=str) + "\n")

    async def refresh(self, keywords: list[str] | None = None, max_per_keyword: int = 20) -> int:
        """Pull fresh opportunities for the given keywords and merge into corpus."""
        keywords = keywords or [
            "artificial intelligence",
            "open source",
            "machine learning",
            "open science",
            "public interest technology",
        ]
        client = await get_client()
        added = 0
        for kw in keywords:
            results = await client.search(keyword=kw, rows=max_per_keyword)
            for opp in results:
                if opp.id not in self._cache:
                    self._persist(opp)
                    added += 1
        logger.info("Corpus refresh complete. Added %d new opportunities.", added)
        return added

    def search_local(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        """Simple local search over the corpus (keyword match)."""
        q = query.lower()
        hits = []
        for item in self._cache.values():
            text = f"{item.get('title','')} {item.get('description','')}".lower()
            if q in text:
                hits.append(item)
        return hits[:limit]

    def stats(self) -> dict[str, Any]:
        return {
            "total": len(self._cache),
            "open_source_relevant": sum(1 for x in self._cache.values() if x.get("open_source_relevant")),
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }
