import uuid
import pytest
from fastapi.testclient import TestClient
from src.search_api.main import app

client = TestClient(app)

tenant_id = str(uuid.uuid4())  # generate a tenant UUID for testing

@pytest.mark.skip(reason="Ollama must be running locally")
def test_full_crud_cycle():
    resource_uuid = str(uuid.uuid4())  # generate a unique resource ID for testing

    # Step 1: CREATE resource
    payload = {
        "resource_uuid": resource_uuid,
        "tenant_uuid": tenant_id,
        "resource_type": "DATABOOK",
        "resource_name": "Patch Test",
        "resource_description": "Original",
        "text": "original text to embed"
    }
    response = client.post("/v1/resource", json=payload)
    assert response.status_code == 201  # resource creation should succeed

    # Step 2: SEARCH for that resource by text and tenant ID
    params = {"q": "original", "tenant_uuid": tenant_id, "max_results": 1}
    response = client.get("/v1/resource", params=params)
    assert response.status_code == 200
    data = response.json()
    assert any(r["resource_uuid"] == resource_uuid for r in data)  # resource should be in result

    # Step 3: PATCH (update) the resource name, description, and embedding
    patch_payload = {
        "resource_name": "Updated Name",
        "resource_description": "Updated Description",
        "text": "new embedded text"  # will re-calculate vector
    }
    response = client.patch(f"/v1/resource/{resource_uuid}", json=patch_payload)
    assert response.status_code == 200  # update should succeed

    # Step 4: DELETE the resource
    response = client.delete(f"/v1/resource/{resource_uuid}")
    assert response.status_code == 200  # deletion should succeed

    # Step 5: Confirm it's gone by searching again
    response = client.get("/v1/resource", params=params)
    assert all(r["resource_uuid"] != resource_uuid for r in response.json())  # should not appear
