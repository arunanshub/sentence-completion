FROM python:3-slim as builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PATH="${PATH}:/root/.local/bin/" \
    # disable dynamic versioning commands (see
    # https://github.com/mtkennerly/poetry-dynamic-versioning?tab=readme-ov-file#environment-variables)
    POETRY_DYNAMIC_VERSIONING_BYPASS="0.0.0"

RUN apt-get update \
    && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock pyproject.toml README.md ./

# install the dependencies first...
RUN --mount=type=cache,target=/root/.cache poetry install --without dev --no-plugins

COPY . .

FROM python:3-slim as runtime

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder /app .

EXPOSE 8000

CMD ["fastapi", "run", "src/sentence_completion/main.py"]
