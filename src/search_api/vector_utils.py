from typing import List
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import httpx
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

SERVICE_ACCOUNT_FILE = "/app/secrets/vertex-sa.json"
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

def fetch_access_token() -> str:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    credentials.refresh(Request())
    return credentials.token

async def get_embedding(text: str) -> List[float]:
    token = fetch_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    json_data = {
        "instances": [
            {
                "task_type": "RETRIEVAL_DOCUMENT",
                "content": text
            }
        ]
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            "https://us-central1-aiplatform.googleapis.com/v1/projects/isdata-staging/locations/us-central1/publishers/google/models/gemini-embedding-001:predict",
            headers=headers,
            json=json_data,
        )
        response.raise_for_status()
        return response.json()["predictions"][0]["embeddings"]["values"]


a
async def search_similar_for_tenant(
    session: AsyncSession,
    query_text: str,
    tenant_uuid: str,
    max_results: int = 10,
    resource_type: Optional[ResourceType] = None,
    include_pending: bool = False,
) -> List[dict]:
    from search_api.vector_utils import get_embedding

    query_embedding = await get_embedding(query_text)

    filters = [Resource.tenant_uuid == tenant_uuid]

    if resource_type:
        filters.append(Resource.resource_type == resource_type)

    if not include_pending:
        filters.append(Resource.embedding_status == EmbeddingStatus.SUCCESS)

    stmt = select(
        Resource.resource_uuid,
        Resource.resource_name,
        Resource.resource_description,
        Resource.resource_type,
        Resource.embedding_status,
        Resource.status_detail,
        func.embedding.op("<=>")(query_embedding).label("distance")
    ).where(
        and_(*filters)
    ).order_by(
        "distance"
    ).limit(max_results)

    result = await session.execute(stmt)
    rows = result.all()

    return [
        {
            "resource_uuid": str(row.resource_uuid),
            "resource_name": row.resource_name,
            "resource_description": row.resource_description,
            "resource_type": row.resource_type,
            "embedding_status": row.embedding_status,
            "status_detail": row.status_detail,
            "similarity_distance": row.distance,
        }
        for row in rows
    ]