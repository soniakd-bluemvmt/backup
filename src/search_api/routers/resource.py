from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks, Path
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from search_api.schemas.resource import ResourceCreate, ResourceSearchResult
from search_api.models.resource import Resource, EmbeddingStatus
from search_api.db import get_db
from search_api.vector import search_similar, get_embedding
from search_api.tasks import embed_resource

router = APIRouter(prefix="/v1/resource", tags=["Resource"])

@router.post("", status_code=202)
def create_resource(
    resource: ResourceCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    db_resource = Resource(
        resource_uuid=resource.resource_uuid,
        tenant_uuid=resource.tenant_uuid,
        resource_type=resource.resource_type,
        resource_name=resource.resource_name,
        resource_description=resource.resource_description,
        embedding_status=EmbeddingStatus.PENDING,
        status_detail=None,
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)

    background_tasks.add_task(embed_resource, db_resource.resource_uuid)

    return {"status": "accepted", "uuid": str(db_resource.resource_uuid)}


@router.get("", response_model=List[ResourceSearchResult])
def search_resources(
    q: str = Query(...),
    max_results: int = Query(10),
    include_pending: bool = Query(False),
    db: Session = Depends(get_db),
):
    query_embedding = get_embedding(q)

    base_query = db.query(Resource)
    if not include_pending:
        base_query = base_query.filter(Resource.embedding_status == EmbeddingStatus.SUCCESS)

    results = search_similar(base_query, query_embedding, max_results)
    return results


@router.get("/{resource_uuid}")
def get_resource_by_uuid(
    resource_uuid: UUID = Path(...),
    db: Session = Depends(get_db),
):
    resource = db.query(Resource).filter(Resource.resource_uuid == resource_uuid).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    return {
        "resource_uuid": str(resource.resource_uuid),
        "resource_name": resource.resource_name,
        "resource_description": resource.resource_description,
        "resource_type": resource.resource_type,
        "embedding_status": resource.embedding_status,
        "status_detail": resource.status_detail,
    }
