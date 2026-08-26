# Glama / local stdio image for OpenGOS MCP.
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir -e . \
    && useradd --create-home --uid 10001 opengos \
    && chown -R opengos:opengos /app

USER opengos
ENV PYTHONUNBUFFERED=1

# Grants.gov / NSF lookups are public HTTP; no secrets required for scoring.
CMD ["opengos"]
