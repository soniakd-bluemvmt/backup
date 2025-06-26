from fastapi import FastAPI
from .models.resource import Base
from .db import engine
from .routers import search

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(search.router, prefix="/api", tags=["search"])


# tests/test_search.py
import pytest
from fastapi.testclient import TestClient
from src.search_api.main import app

client = TestClient(app)

@pytest.mark.skip(reason="Ollama must be running locally")
def test_post_search():
    resp = client.post("/api/search", params={"text": "What is mental health?"})
    assert resp.status_code == 200
    data = resp.json()
    assert "embedding" in data

@pytest.mark.skip(reason="Requires search entry to exist")
def test_delete_search():
    uuid_to_delete = "some-uuid-here"
    resp = client.delete(f"/api/search/{uuid_to_delete}")
    assert resp.status_code in [200, 404]
