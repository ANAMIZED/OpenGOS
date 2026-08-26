"""Allow running as python -m opengos over MCP stdio."""

from opengos.server import mcp


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
