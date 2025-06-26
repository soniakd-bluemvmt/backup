from fastapi import FastAPI
from .models.resource import Base
from .db import engine
from .routers import search

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(search.router, prefix="/api", tags=["search"])


