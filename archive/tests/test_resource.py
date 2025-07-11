import pytest
from fastapi.testclient import TestClient
from search_api.main import app
from uuid import uuid4

client = TestClient(app)


def test_create_resource():
    payload = {
        "resource_uuid": str(uuid4()),
        "tenant_uuid": str(uuid4()),
        "resource_type": "DATASOURCE",
        "resource_name": "Test Resource",
        "resource_description": "A resource used for testing"
    }
    response = client.post("/v1/resource", json=payload)
    assert response.status_code == 201
    json_data = response.json()
    assert "status" in json_data and json_data["status"] == "created"
    assert "uuid" in json_data


def test_search_resources():
    # First, create a resource
    resource_payload = {
        "resource_uuid": str(uuid4()),
        "tenant_uuid": str(uuid4()),
        "resource_type": "DATASOURCE",
        "resource_name": "Searchable Resource",
        "resource_description": "Contains some searchable content"
    }
    create_resp = client.post("/v1/resource", json=resource_payload)
    assert create_resp.status_code == 201

    # Now search with a query that should match roughly
    search_resp = client.get("/v1/resource", params={"q": "searchable", "max_results": 5})
    assert search_resp.status_code == 200
    results = search_resp.json()
    assert isinstance(results, list)
    if results:
        # Check one item shape
        item = results[0]
        assert "resource_uuid" in item
        assert "resource_name" in item
        assert "resource_description" in item
        assert "resource_type" in item
        assert "score" in item
