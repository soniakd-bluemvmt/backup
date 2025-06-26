from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from ..db import get_db
from ..models.resource import Resource
from ..schemas.resource import ResourceCreate, ResourceRead
from ..ollama_client import get_embedding_from_ollama

router = APIRouter()

@router.post("/v1/resource", status_code=201)
def create_resource(payload: ResourceCreate, db: Session = Depends(get_db)):
    embedding = get_embedding_from_ollama(payload.text)
    resource = Resource(
        resource_uuid=payload.resource_uuid,
        resource_type=payload.resource_type,
        resource_name=payload.resource_name,
        resource_description=payload.resource_description,
        embedding=embedding
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return {"message": "Resource created"}

@router.get("/v1/resource", response_model=list[ResourceRead])
def search_resources(q: str, max_results: int = 5, db: Session = Depends(get_db)):
    embedding = get_embedding_from_ollama(q)
    stmt = select(Resource).order_by(Resource.embedding.l2_distance(embedding)).limit(max_results)
    return db.execute(stmt).scalars().all()
