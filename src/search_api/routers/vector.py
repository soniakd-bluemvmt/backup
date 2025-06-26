from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from ..db import get_db
from ..models.resource import Search
from ..schemas.resource import SearchSchema
from ..ollama_client import get_embedding_from_ollama
from sqlalchemy import func, select

router = APIRouter()

@router.post("/search", response_model=SearchSchema)
def create_search(text: str, db: Session = Depends(get_db)):
    embedding = get_embedding_from_ollama(text)
    search_entry = Search(
        uuid=uuid.uuid4(),
        json={"text": text},
        create_date=func.now(),
        last_update_date=func.now(),
        embedding=embedding,
        resource_uuid=None
    )
    db.add(search_entry)
    db.commit()
    db.refresh(search_entry)
    return search_entry

@router.delete("/search/{uuid}")
def delete_search(uuid: UUID, db: Session = Depends(get_db)):
    search = db.get(Search, uuid)
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")
    db.delete(search)
    db.commit()
    return {"detail": "Deleted"}

@router.get("/search", response_model=list[SearchSchema])
def search_vector(q: str = Query(...), db: Session = Depends(get_db)):
    embedding = get_embedding_from_ollama(q)
    stmt = select(Search).order_by(Search.embedding.l2_distance(embedding)).limit(5)
    results = db.execute(stmt).scalars().all()
    return results
