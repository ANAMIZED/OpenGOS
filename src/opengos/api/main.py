"""OpenGOS FastAPI application."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="OpenGOS",
    description="Grants discovery, ranking, drafting, and public-goods funding API.",
    version="0.4.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
def health():
    return {"status": "ok", "service": "opengos", "version": "0.4.0"}


@app.get("/v1/status")
def status():
    return {
        "service": "opengos",
        "version": "0.4.0",
        "surfaces": ["mcp", "cli", "sdk", "api", "multi-agent"],
    }


@app.get("/v1/grants/search")
def search_grants(q: str = "", limit: int = 10):
    return {"query": q, "limit": limit, "results": [], "mode": "mock"}


@app.post("/v1/proposals/draft")
def draft_proposal(body: dict):
    return {
        "opportunity_id": body.get("opportunity_id"),
        "outline": ["Summary", "Need", "Approach", "Budget", "Impact"],
        "mode": "mock",
    }


@app.post("/v1/workflows")
def workflow(goal: str = "discover-and-draft"):
    return {
        "goal": goal,
        "agents": ["discoverer", "ranker", "drafter"],
        "status": "accepted",
        "mode": "mock",
    }


def run():
    import uvicorn

    uvicorn.run("opengos.api.main:app", host="0.0.0.0", port=8080, reload=False)


if __name__ == "__main__":
    run()
