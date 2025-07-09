import os
import httpx
import json
from typing import List, Dict, Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, text
from sqlalchemy import func

from pgvector.sqlalchemy import Vector
from search_api.models.resource import Resource
from search_api.schemas.resource import ResourceType
from search_api.models.resource import EmbeddingStatus


LITELLM_HOST = os.getenv("LITELLM_HOST", "http://litellm:4000")
LITELLM_MODEL = os.getenv("LITELLM_MODEL", "gemini-embedding")
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")


async def get_embedding(text: str) -> list[float]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{LITELLM_HOST}/embeddings",
            json={"model": LITELLM_MODEL, "input": text},
        )
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]


async def search_similar_for_tenant(
    session: AsyncSession,
    query_text: str,
    tenant_uuid: str,
    max_results: int = 10,
    resource_type: Optional[ResourceType] = None,
    include_pending: bool = False,
) -> List[Resource]:
    embedding = await get_embedding(query_text)

    stmt = select(
        Resource,
        (1 - Resource.embedding.cosine_distance(embedding)).label("score")
    ).filter(Resource.tenant_uuid == tenant_uuid)

    if not include_pending:
        stmt = stmt.filter(Resource.embedding_status == EmbeddingStatus.SUCCESS)

    if resource_type:
        stmt = stmt.filter(Resource.resource_type == resource_type)

    stmt = stmt.order_by(text("score DESC")).limit(max_results)

    result = await session.execute(stmt)
    return [row[0] for row in result.fetchall()]
