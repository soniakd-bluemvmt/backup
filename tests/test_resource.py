import uuid
import pytest
from fastapi.testclient import TestClient
from src.search_api.main import app

client = TestClient(app)

@pytest.mark.skip(reason="Ollama must be running locally")
def test_create_resource():
    payload = {
        "resource_uuid": str(uuid.uuid4()),
        "resource_type": "DATABOOK",
        "resource_name": "Test Book",
        "resource_description": "A sample databook",
        "text": "How to stay mentally healthy"
    }
    response = client.post("/v1/resource", json=payload)
    assert response.status_code == 201

@pytest.mark.skip(reason="Requires embedding + existing resource")
def test_search_resources():
    response = client.get("/v1/resource", params={"q": "mental health tips", "max_results": 3})
    assert response.status_code == 200
    assert isinstance(response.json(), list)



