"""Continuous ingestion and multi-source discovery for OpenGOS."""

from .corpus import CorpusManager, refresh

__all__ = ["CorpusManager", "refresh"]
