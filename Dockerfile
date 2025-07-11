FROM python:3.12-slim

# Install build dependencies for compiling greenlet and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip install --no-cache-dir poetry==2.1.3
RUN python -m poetry config virtualenvs.create false \
    && python -m poetry install --extras "proxy" --no-interaction --no-ansi


WORKDIR /app

COPY pyproject.toml ./ 
COPY src ./src
COPY docker/entrypoint.sh /app/entrypoint.sh
COPY src/alembic /app/alembic
COPY alembic.ini /app/alembic.ini
COPY docker/check_db.py ./docker/check_db.py
COPY config.yaml /app/config.yaml


RUN python -m poetry config virtualenvs.create false \
    && python -m poetry install --no-interaction --no-ansi

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["sh", "/app/entrypoint.sh"]

CMD ["poetry", "run", "uvicorn", "src.search_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
