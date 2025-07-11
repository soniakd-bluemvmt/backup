from google.auth.transport.requests import Request
from google.oauth2 import service_account
import httpx
import json

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
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://us-central1-aiplatform.googleapis.com/v1/projects/isdata-staging/locations/us-central1/publishers/google/models/gemini-embedding-001:predict",
            headers=headers,
            json=json_data,
        )
        response.raise_for_status()
        return response.json()["predictions"][0]["embeddings"]["values"]
