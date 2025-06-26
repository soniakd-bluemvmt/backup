from fastapi import FastAPI
from .routers import vector
from .models.vector import Base
from .db import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(vector.router, prefix="/api", tags=["vectors"])


# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . .

CMD ["uvicorn", "src.search_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
