# Stage 1: Configuring base image
FROM simbachain/poetry-3.10 AS base

WORKDIR /app

COPY ./pyproject.toml /app
COPY ./poetry.lock /app
COPY ./backend /app

RUN python -m pip install --upgrade pip && \
    poetry install --without dev,test

# Stage 2: Production environment with source code
FROM base AS trained
# RUN poetry run spacy download en_core_web_sm
RUN poetry run rasa train

# Stage 3: Production environment with source code
FROM trained AS production
CMD ["poetry", "run", "rasa", "run", "--enable-api", "--cors", "*", "--port" ,"5005"]
