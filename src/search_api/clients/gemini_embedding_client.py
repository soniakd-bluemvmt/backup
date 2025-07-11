import os
import requests

def get_gemini_embedding(text: str, project_id: str = "isdata-staging", location: str = "us-central1") -> list[float]:
    VERTEX_ACCESS_TOKEN = os.getenv("VERTEX_ACCESS_TOKEN")
    if not access_token:
        raise RuntimeError("ACCESS_TOKEN environment variable is not set")

    url = (
        f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/publishers/google/models/gemini-embedding-001:predict"
    )

    headers = {
    "Authorization": f"Bearer {VERTEX_ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

    data = {
        "instances": [
            {
                "task_type": "RETRIEVAL_DOCUMENT",
                "content": text,
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    response_json = response.json()
    embeddings = response_json["predictions"][0]["embeddings"]["values"]

    return embeddings


# Example usage
if __name__ == "__main__":
    text = "Hello from Gemini embedding test!"
    vector = get_gemini_embedding(text)
    print(f"Embedding vector (length {len(vector)}): {vector[:10]}...")  # Print first 10 values
