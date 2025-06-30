FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . .

CMD ["poetry", "run", "uvicorn", "src.search_api.main:app", "--host", "0.0.0.0", "--port", "8000"]

