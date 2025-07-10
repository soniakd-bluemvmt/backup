from search_api.models.resource import Base
from sqlalchemy.ext.asyncio import create_async_engine
from fastapi import FastAPI

async_engine = create_async_engine(
    "postgresql+asyncpg://postgres:thisispostgres@postgresql:5432/search_db",
    echo=True,
)

async def async_create_all():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await async_create_all()
