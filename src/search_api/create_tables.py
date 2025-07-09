from search_api.models.resource import Base  # precise import

# your engine creation here, e.g.
from sqlalchemy.ext.asyncio import create_async_engine

async_engine = create_async_engine(
    "postgresql+asyncpg://bluemvmt:thisispostgres@db:5432/search_db",
    echo=True,
)

import asyncio

async def async_create_all():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(async_create_all())
