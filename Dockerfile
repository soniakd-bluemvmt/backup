FROM python:3.12

WORKDIR /app

# Copy project metadata first
COPY pyproject.toml poetry.lock* ./

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev python3-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --upgrade pip && pip install poetry==1.8.2

# Required in your case to prevent install crash
RUN pip install numpy --no-cache-dir


COPY src ./src

# Install Python deps
RUN poetry install --no-interaction --no-ansi --with dev --only main --verbose

COPY config.yaml .
COPY alembic.ini .
COPY docker/entrypoint.sh .
COPY docker/check_db.py ./docker/check_db.py

RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]

CMD ["poetry", "run", "uvicorn", "src.search_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
