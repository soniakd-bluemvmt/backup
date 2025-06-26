from pydantic import BaseModel
from typing import List

class VectorCreate(BaseModel):
    name: str
    vector: List[float]

class VectorRead(VectorCreate):
    id: int

    class Config:
        from_attributes = True


