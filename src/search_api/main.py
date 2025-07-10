from fastapi import FastAPI
from .models.resource import Base
from .db import engine
from .routers import resource
from .create_tables import async_create_all  # Import the correct async function

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await async_create_all()  # Run your async table creation here

app.include_router(resource.router)  # Register resource routes under /v1/resource (or whatever path)
