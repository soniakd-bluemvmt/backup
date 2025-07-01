from fastapi import FastAPI
from .models.resource import Base
from .db import engine
from .routers import resource

Base.metadata.create_all(bind=engine)  # auto-create tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables()

    
app.include_router(resource.router)  # register /v1/resource endpoints