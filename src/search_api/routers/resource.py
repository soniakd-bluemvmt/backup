from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List
from search_api.schemas.resource import ResourceCreate, ResourceSearchResult
from search_api.models.resource import Resource, ResourceType
from search_api.db import get_db
from search_api.vector import get_embedding, search_similar

router = APIRouter(prefix="/v1/resource", tags=["Resource"])


@router.post("", status_code=201)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    embedding = get_embedding(resource.resource_description or resource.resource_name)
    db_resource = Resource(
        resource_uuid=resource.resource_uuid,
        tenant_uuid=resource.tenant_uuid,
        resource_type=resource.resource_type,
        resource_name=resource.resource_name,
        resource_description=resource.resource_description,
        embedding=embedding
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return {"status": "created", "uuid": str(db_resource.uuid)}


@router.get("", response_model=List[ResourceSearchResult])
def search_resources(
    q: str = Query(...),
    max_results: int = Query(10),
    db: Session = Depends(get_db)
):
    query_embedding = get_embedding(q)
    results = search_similar(db, query_embedding, max_results)
    return results
