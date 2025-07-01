import httpx

import os

LITELLM_HOST = os.getenv("LITELLM_HOST", "http://litellm:4000")
LITELLM_MODEL = os.getenv("LITELLM_MODEL", "openai-gpt-4o")

async def get_embedding_litellm(text: str) -> list[float]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{LITELLM_HOST}/embeddings",
            json={
                "model": LITELLM_MODEL,
                "input": text,
            },
        )
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]
