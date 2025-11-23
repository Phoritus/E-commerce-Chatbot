FROM python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.9.10 /uv /uvx /bin/

ADD . /app

WORKDIR /app

RUN uv sync --locked

EXPOSE 80

CMD ["uv", "run"]