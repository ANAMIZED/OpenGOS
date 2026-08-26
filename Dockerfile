# Glama inspects MCP over stdio.
# Admin generator: build ["pip install --no-cache-dir ."]
#                  CMD   ["python", "-m", "opengos"]
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir . \
    && useradd --create-home --uid 10001 --shell /usr/sbin/nologin mcp \
    && chown -R mcp:mcp /app

USER mcp

CMD ["python", "-m", "opengos"]
