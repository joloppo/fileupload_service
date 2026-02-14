FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --no-dev --no-install-project --frozen

# Dependency separation for layer caching
COPY src ./src
RUN uv sync --locked --no-dev

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "fileupload_service.app:build_app", "--host", "0.0.0.0", "--port", "8000", "--limit-concurrency", "200", "--workers", "4"]

