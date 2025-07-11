FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev python3-dev curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install poetry==1.8.2

COPY pyproject.toml poetry.lock* ./
COPY src ./src

RUN poetry install --no-interaction --no-ansi --verbose

RUN poetry show psycopg2-binary

COPY config.yaml .
COPY alembic.ini .
COPY docker/entrypoint.sh .
COPY docker/check_db.py ./docker/check_db.py

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
