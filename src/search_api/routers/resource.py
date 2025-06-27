from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from ..db import get_db
from ..models.resource import Resource
from ..schemas.resource import ResourceCreate, ResourceRead, ResourceUpdate
from ..ollama_client import get_embedding_from_ollama

router = APIRouter()

@router.post("/v1/resource", status_code=201)
def create_resource(payload: ResourceCreate, db: Session = Depends(get_db)):
    embedding = get_embedding_from_ollama(payload.text)
    resource = Resource(
        resource_uuid=payload.resource_uuid,
        tenant_uuid=payload.tenant_uuid,
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
def search_resources(q: str, tenant_uuid: UUID, max_results: int = 5, db: Session = Depends(get_db)):
    embedding = get_embedding_from_ollama(q)
    stmt = select(Resource, Resource.embedding.l2_distance(embedding).label("score"))\
        .where(Resource.tenant_uuid == tenant_uuid)\
        .order_by("score")\
        .limit(max_results)
    results = db.execute(stmt).all()
    return [
        ResourceRead(
            resource_uuid=row.Resource.resource_uuid,
            resource_name=row.Resource.resource_name,
            resource_description=row.Resource.resource_description,
            resource_type=row.Resource.resource_type,
            score=row.score
        )
        for row in results
    ]

@router.patch("/v1/resource/{resource_uuid}")
def update_resource(resource_uuid: UUID, update: ResourceUpdate, db: Session = Depends(get_db)):
    resource = db.scalar(select(Resource).where(Resource.resource_uuid == resource_uuid))
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    if update.resource_name is not None:
        resource.resource_name = update.resource_name
    if update.resource_description is not None:
        resource.resource_description = update.resource_description
    if update.text is not None:
        resource.embedding = get_embedding_from_ollama(update.text)

    db.commit()
    db.refresh(resource)
    return {"message": "Resource updated"}

@router.delete("/v1/resource/{resource_uuid}")
def delete_resource(resource_uuid: UUID, db: Session = Depends(get_db)):
    resource = db.scalar(select(Resource).where(Resource.resource_uuid == resource_uuid))
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(resource)
    db.commit()
    return {"message": "Resource deleted"}
