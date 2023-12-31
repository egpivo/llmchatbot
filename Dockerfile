FROM python:3.10-slim-buster as base

ENV POETRY_HOME=/root/.poetry \
    POETRY_VERSION=1.6.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /chatbot

FROM base as builder

RUN apt-get update && \
    apt-get install -y make libsndfile1 && \
    apt-get install gcc -y && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir poetry==${POETRY_VERSION} && \
    poetry config installer.max-workers 10 && \
    poetry install --only=main --no-root && \
    poetry build

FROM base as final

#COPY . ./
COPY --from=builder /chatbot/.venv ./.venv
COPY --from=builder /chatbot/dist/ .
COPY chatbot/app.py ./chatbot/app.py
COPY scripts ./scripts
COPY envs ./envs

RUN ./.venv/bin/pip install *.whl

# Add metadata labels
LABEL maintainer="Joseph Wang <egpivo@gmail.com>" \
      description="Docker image for Chatbot application" \
      version="1.0.2"

ENTRYPOINT ["/bin/bash", "-c", "source .venv/bin/activate && scripts/run_app_service.sh --is_production"]
