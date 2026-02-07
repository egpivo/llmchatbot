FROM python:3.10-slim-bullseye as base

ENV POETRY_HOME=/root/.poetry \
    POETRY_VERSION=1.6.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /llmchatbot

FROM base as builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        make \
        libsndfile1 \
        gcc && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir poetry==${POETRY_VERSION} && \
    poetry config installer.max-workers 10 && \
    poetry install --only=main --no-root && \
    poetry build

FROM base as final

COPY --from=builder /llmchatbot/.venv ./.venv
COPY --from=builder /llmchatbot/dist/ .
COPY llmchatbot/app.py ./llmchatbot/app.py
COPY scripts ./scripts
COPY envs ./envs

RUN ./.venv/bin/pip install *.whl

LABEL maintainer="Joseph Wang <egpivo@gmail.com>" \
      description="Docker image for Chatbot application" \
      version="1.0.4"

ENTRYPOINT ["/bin/bash", "-c", "source .venv/bin/activate && scripts/run_app_service.sh --is_production"]
