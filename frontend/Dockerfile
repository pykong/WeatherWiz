FROM simbachain/poetry-3.10 AS base

WORKDIR /app

COPY ./frontend /app

CMD ["python", "-m", "http.server", "8000"]
