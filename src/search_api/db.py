import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SyncSession
from fastapi import Depends

# Read individual DB params
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")  # empty
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "search_db")

def make_db_url(user, password, host, port, dbname, async_=True):
    driver = "postgresql+asyncpg" if async_ else "postgresql"
    if password:  # only add password if set and non-empty
        return f"{driver}://{user}:{password}@{host}:{port}/{dbname}"
    else:
        return f"{driver}://{user}@{host}:{port}/{dbname}"

ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL") or make_db_url(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, async_=True)
SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL") or make_db_url(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, async_=False)

# Async engine and sessionmaker
engine = create_async_engine(ASYNC_DATABASE_URL, future=True, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

# Sync engine and sessionmaker
sync_engine = create_engine(SYNC_DATABASE_URL)
SessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)


