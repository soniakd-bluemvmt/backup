Vector similarity search API using FastAPI, PostgreSQL + pgvector, and Ollama for embedding.

## Setup

```bash
poetry install
poetry run uvicorn src.search_api.main:app --reload
```

Ensure Ollama is running locally with an embedding model like `mxb` or `mxb-large`:

```bash
ollama run mxb
```

---

## API Endpoints

### Create a Resource
```http
POST /v1/resource
```

#### Request JSON
```json
{
  "resource_uuid": "<uuid>",
  "tenant_uuid": "<uuid>",
  "resource_type": "DATABOOK",
  "resource_name": "My Document",
  "resource_description": "Optional description",
  "text": "This is the content to embed."
}
```

#### Response
```json
{
  "message": "Resource created"
}
```

---

### Search for a Resource
```http
GET /v1/resource?q=<search text>&tenant_uuid=<uuid>&max_results=5
```

#### Response
```json
[
  {
    "resource_uuid": "...",
    "resource_name": "...",
    "resource_description": "...",
    "resource_type": "DATABOOK",
    "score": 0.03
  }
]
```

---

### Update a Resource
```http
PATCH /v1/resource/{resource_uuid}
```

#### Request JSON
```json
{
  "resource_name": "Updated Name",
  "resource_description": "Updated Description",
  "text": "New text to re-embed"
}
```

#### Response
```json
{
  "message": "Resource updated"
}
```

---

### Delete a Resource
```http
DELETE /v1/resource/{resource_uuid}
```

#### Response
```json
{
  "message": "Resource deleted"
}
```
