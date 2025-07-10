import asyncio
import httpx

LITELLM_HOST = "http://localhost:4000"
LITELLM_MODEL = "gemini-embedding"

async def test_embedding():
    text = "Hello from Gemini embedding test!"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{LITELLM_HOST}/embeddings",
            json={
                "model": LITELLM_MODEL,
                "input": text,
            },
        )
        response.raise_for_status()
        data = response.json()
        print("Embedding response:", data)
        embedding = data["data"][0]["embedding"]
        print(f"Embedding vector length: {len(embedding)}")
        print(f"Sample values: {embedding[:5]}")

if __name__ == "__main__":
    asyncio.run(test_embedding())
