"""OpenGOS CLI."""
from __future__ import annotations

import typer
from rich import print as rprint

app = typer.Typer(name="opengos-cli", help="OpenGOS CLI — grants discovery & drafting")


@app.command()
def version() -> None:
    rprint("[bold]OpenGOS[/bold] 0.4.0")


@app.command()
def status() -> None:
    rprint({"service": "opengos", "version": "0.4.0", "mcp": True, "api": True, "sdk": True})


@app.command()
def search(query: str = typer.Argument(..., help="Keyword search")) -> None:
    rprint({"query": query, "mode": "mock", "results": []})
    rprint("[dim]Use MCP `search_grants` or API for live Grants.gov.[/dim]")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
