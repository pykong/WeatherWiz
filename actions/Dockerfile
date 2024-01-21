# Stage 1: Configuring base image
FROM simbachain/poetry-3.10 AS base

WORKDIR /app

COPY ./pyproject.toml /app
COPY ./poetry.lock /app
COPY ./actions /app

RUN python -m pip install --upgrade pip && \
    poetry install --without dev,test

# Stage 2: Production environment with source code
FROM base AS production
CMD ["poetry", "run", "rasa", "run", "actions", "--actions", "actions"]
