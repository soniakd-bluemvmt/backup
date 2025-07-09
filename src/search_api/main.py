from fastapi import FastAPI
from .models.resource import Base
from .db import engine
from .routers import resource
from .create_tables import create_tables

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_tables()

app.include_router(resource.router)  # register /v1/resource endpoints
