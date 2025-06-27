from fastapi import APIRouter, Depends, HTTPException, Query, Path, Request, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from ..db import get_db
from ..models.resource import Resource
from ..schemas.resource import ResourceCreate, ResourceRead, ResourceUpdate
from ..ollama_client import get_embedding_from_ollama
from ..auth import verify_tenant
from ..logger import logger

router = APIRouter()

@router.post("/v1/resource", status_code=201)
def create_resource(payload: ResourceCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Store with dummy vector first, update later
    placeholder = [0.0] * 1536
    resource = Resource(
        resource_uuid=payload.resource_uuid,
        tenant_uuid=payload.tenant_uuid,
        resource_type=payload.resource_type,
        resource_name=payload.resource_name,
        resource_description=payload.resource_description,
        embedding=placeholder
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)

    background_tasks.add_task(update_embedding, payload.text, resource.uuid, db)
    logger.info(f"CREATE {payload.resource_uuid} by tenant {payload.tenant_uuid}")
    return {"message": "Resource created"}

def update_embedding(text: str, uuid_: UUID, db: Session):
    embedding = get_embedding_from_ollama(text)
    resource = db.scalar(select(Resource).where(Resource.uuid == uuid_))
    if resource:
        resource.embedding = embedding
        db.commit()

@router.get("/v1/resource", response_model=list[ResourceRead])
def search_resources(q: str, tenant_uuid: UUID = Depends(verify_tenant), max_results: int = 5, db: Session = Depends(get_db)):
    embedding = get_embedding_from_ollama(q)
    stmt = select(Resource, Resource.embedding.l2_distance(embedding).label("score"))\
        .where(Resource.tenant_uuid == tenant_uuid)\
        .order_by("score")\
        .limit(max_results)
    results = db.execute(stmt).all()
    logger.info(f"SEARCH tenant={tenant_uuid} q='{q}'")
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
def update_resource(resource_uuid: UUID, update: ResourceUpdate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    resource = db.scalar(select(Resource).where(Resource.resource_uuid == resource_uuid))
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    if update.resource_name is not None:
        resource.resource_name = update.resource_name
    if update.resource_description is not None:
        resource.resource_description = update.resource_description
    if update.text is not None:
        background_tasks.add_task(update_embedding, update.text, resource.uuid, db)

    db.commit()
    db.refresh(resource)
    logger.info(f"UPDATE {resource_uuid}")
    return {"message": "Resource updated"}

@router.delete("/v1/resource/{resource_uuid}")
def delete_resource(resource_uuid: UUID, db: Session = Depends(get_db)):
    resource = db.scalar(select(Resource).where(Resource.resource_uuid == resource_uuid))
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(resource)
    db.commit()
    logger.info(f"DELETE {resource_uuid}")
    return {"message": "Resource deleted"}