FROM python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.9.10 /uv /uvx /bin/

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY . .

RUN uv sync --locked

ENV PATH="/app/.venv/bin:${PATH}"

EXPOSE 80


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]