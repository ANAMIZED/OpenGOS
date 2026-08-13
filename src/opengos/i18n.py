"""
Phase 1 Multilingual support for OpenGOS.

- Language metadata on opportunities
- Lightweight keyword expansion for common open-source / AI terms
  across major languages used in public-goods funding ecosystems.
"""

from __future__ import annotations

KEYWORD_EXPANSIONS: dict[str, list[str]] = {
    "open source": [
        "open source",
        "opensource",
        "open-source",
        "código abierto",
        "codigo abierto",
        "logiciel libre",
        "code source ouvert",
        "open source software",
        "oss",
        "livre",
        "software livre",
        "オープンソース",
        "开源",
        "오픈소스",
    ],
    "artificial intelligence": [
        "artificial intelligence",
        "ai",
        "machine learning",
        "ml",
        "llm",
        "inteligencia artificial",
        "apprentissage automatique",
        "apprentissage profond",
        "apprentissage machine",
        "人工知能",
        "人工智能",
        "인공지능",
    ],
    "public goods": [
        "public goods",
        "public-goods",
        "bienes públicos",
        "biens publics",
        "public interest",
        "interés público",
        "intérêt public",
        "commons",
        "digital public goods",
    ],
    "grant": [
        "grant",
        "grants",
        "funding",
        "subvention",
        "subvención",
        "förderung",
        "finanzierung",
        "bolsa",
        "edital",
    ],
}


def expand_keywords(query: str) -> list[str]:
    """Return the original query plus expanded variants for better recall."""
    q = query.lower().strip()
    expanded = {q}
    for key, variants in KEYWORD_EXPANSIONS.items():
        if key in q or any(v in q for v in variants[:3]):
            expanded.update(variants)
    return list(expanded)


def detect_language_hint(text: str) -> str:
    """Very lightweight language hint (Phase 1). Defaults to 'en'."""
    if not text:
        return "en"
    t = text.lower()
    if any(c in t for c in "áéíóúñ¿¡"):
        return "es"
    if any(w in t for w in ("le ", "la ", "les ", "des ", "une ", "pour ")):
        return "fr"
    if any(w in t for w in ("der ", "die ", "das ", "und ", "für ")):
        return "de"
    return "en"
