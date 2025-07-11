import os
import httpx
from typing import List

LITELLM_BASE_URL = os.getenv("LITELLM_BASE_URL", "http://litellm:30264")
LITELLM_MODEL = os.getenv("LITELLM_MODEL", "gemini-embedding-001")

async def get_embedding(text: str) -> List[float]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{LITELLM_BASE_URL}/v1/embeddings",
            json={"input": text, "model": LITELLM_MODEL},
        )
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]
