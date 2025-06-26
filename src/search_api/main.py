from fastapi import FastAPI
from .routers import vector
from .models.vector import Base
from .db import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(vector.router, prefix="/api", tags=["vectors"])
