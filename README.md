# Vector similarity search API using FastAPI, PostgreSQL + pgvector, and Ollama for embedding.

## Setup

Make sure you have Docker and Docker Compose installed.

### 1. Start PostgreSQL with pgvector enabled

Use a PostgreSQL Docker image that includes pgvector, e.g.:

```yaml
services:
  postgresql:
    image: vshefferbluemvmt/postgresql-16-pgvector:latest
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 
      POSTGRES_DB: search_db
    ports:
      - "5432:5432"

Ensure pgvector extension is created once your DB is running:

sql
CREATE EXTENSION IF NOT EXISTS vector;


Create or confirm the Docker network bluemvmt exists:
docker network ls
docker network create bluemvmt

### 2. RUN API

docker compose up --build



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
