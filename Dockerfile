FROM python:3.10-buster as builder

RUN pip install --no-cache-dir --user poetry==1.6.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PATH="${PATH}:/root/.local/bin"

WORKDIR /chatbot

COPY . ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry config installer.max-workers 10 && \
    poetry install

# Runtime stage
FROM python:3.10-slim-buster as runtime

RUN apt-get update && \
    apt-get install -y make libsndfile1 && \
    apt-get install -y make && \
    rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/chatbot/.venv \
    PATH="/chatbot/.venv/bin:$PATH"

WORKDIR /chatbot

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY . /chatbot

# Add metadata labels
LABEL maintainer="Your Name <your.email@example.com>" \
      description="Docker image for Chatbot application" \
      version="1.0"

ENTRYPOINT ["/bin/bash", "-c", "source $VIRTUAL_ENV/bin/activate && make serve"]
