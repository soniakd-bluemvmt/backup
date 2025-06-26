from testcontainers.postgres import PostgresContainer
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.search_api.models.resource import Base

@pytest.fixture(scope="session")
def pgvector_container():
    with PostgresContainer("ankane/pgvector") as postgres:
        postgres.start()
        os.environ["DATABASE_URL"] = postgres.get_connection_url()
        engine = create_engine(postgres.get_connection_url())
        Base.metadata.create_all(engine)
        yield postgres

@pytest.fixture(scope="function")
def db_session(pgvector_container):
    engine = create_engine(os.getenv("DATABASE_URL"))
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()