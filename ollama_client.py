def get_embedding_from_ollama(text: str, model: str = "mxb") -> list[float]:
    url = "http://localhost:11434/api/embeddings"
    payload = {"model": model, "input": text}  # Change "prompt" → "input"
    resp = requests.post(url, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["embeddings"][0]["embedding"]  # Access embedding inside nested structure
