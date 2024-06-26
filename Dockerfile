FROM python:3-slim as builder

WORKDIR /app

ARG APP_VERSION

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PATH="${PATH}:/root/.local/bin/" \
    # disable dynamic versioning commands (see
    # https://github.com/mtkennerly/poetry-dynamic-versioning?tab=readme-ov-file#environment-variables)
    POETRY_DYNAMIC_VERSIONING_BYPASS=${APP_VERSION}

RUN apt-get update \
    && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock pyproject.toml README.md ./

# install the dependencies first...
RUN --mount=type=cache,target=/root/.cache poetry install --without dev --no-plugins

COPY . .

FROM python:3-slim as runtime

WORKDIR /app

RUN apt-get update && apt-get install -y curl

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    HF_HUB_CACHE="/app/.cache/huggingface/hub"

COPY --from=builder /app .

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/_health || exit 1

CMD ["fastapi", "run", "src/sentence_completion/main.py"]
