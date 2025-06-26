from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas.vector import VectorCreate, VectorRead
from ..models.vector import Vector
from ..db import get_db

router = APIRouter()

@router.post("/vectors/", response_model=VectorRead)
def create_vector(vector: VectorCreate, db: Session = Depends(get_db)):
    db_vector = Vector(**vector.model_dump())
    db.add(db_vector)
    db.commit()
    db.refresh(db_vector)
    return db_vector

@router.get("/vectors/", response_model=list[VectorRead])
def list_vectors(db: Session = Depends(get_db)):
    return db.query(Vector).all()


# src/search_api/main.py
from fastapi import FastAPI
from .routers import vector
from .models.vector import Base
from .db import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(vector.router, prefix="/api", tags=["vectors"])
