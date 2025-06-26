from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

class VectorCreate(BaseModel):
    name: str
    vector: List[float]

class VectorRead(VectorCreate):
    id: int

    class Config:
        from_attributes = True

class DatasourceSchema(BaseModel):
    uuid: uuid.UUID
    source_url: str
    unique_name: str
    long_description: str
    create_date: datetime
    json: dict

class FileLoadedSchema(BaseModel):
    uuid: uuid.UUID
    datasource_uuid: uuid.UUID
    create_date: datetime
    last_update_date: datetime
    json: dict

class SearchSchema(BaseModel):
    uuid: uuid.UUID
    json: dict
    create_date: datetime
    last_update_date: datetime
    embedding: List[float]
    datasource_uuid: uuid.UUID

class Llama2SearchSchema(SearchSchema):
    embedding: List[float]  # still vector but of dim 1024


# src/search_api/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/search_db")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

