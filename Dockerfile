FROM python:3.10.12

ENV POETRY_HOME=/root/.poetry \
    POETRY_VERSION=1.6.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /chatbot

RUN apt-get update && \
    apt-get install -y make libsndfile1 && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir poetry==${POETRY_VERSION} && \
    poetry config installer.max-workers 10 && \
    poetry install

# Add metadata labels
LABEL maintainer="Joseph Wang <egpivo@gmail.com>" \
      description="Docker image for Chatbot application" \
      version="1.0.1"

ENTRYPOINT ["/bin/bash", "-c", "source $(poetry env info --path)/bin/activate && make local-serve"]
