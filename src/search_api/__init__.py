"""
This module contains the initialization code for the FastAPI application.
"""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()

log_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
}


log_level = log_levels[os.environ.get("LOG_LEVEL", "WARNING")]
logging.basicConfig(level=log_level)
log = logging.getLogger("init")

db_info = {
    "db_host": os.environ.get("DB_HOSTNAME", "postgresql.db"),
    "db_user": os.environ.get("DB_USER", "postgres"),
    "db_port": os.environ.get("DB_PORT", 5432),
    "db_password": os.environ.get("DB_PASSWORD"),
    "db_name": os.environ.get("DB_NAME", "datasource_api"),
}

db_url = (
    f"postgresql+asyncpg://{db_info['db_user']}:"
    f"{db_info['db_password']}@"
    f"{db_info['db_host']}:"
    f"{db_info['db_port']}/"
    f"{db_info['db_name']}"
)

try:
    log.info(f"connecting to database: {db_url}")
    engine = create_async_engine(db_url)
except Exception as e:
    log.error(f"error connecting to database: {e}")
    raise e

SessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for the application lifespan.
    """
    yield


async def get_db_session():
    """
    Yields a database session and ensures it is closed after use.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()

app = FastAPI(
    version="0.1.0",
    root_path="/v1",
    docs_url="/docs",
    description="The Search API handles all bluai searches.",
    title="Search API",
    summary="API adding resources to search as well as handling the searching, itself.",
    lifespan=lifespan,
    separate_input_output_schemas=False
)
