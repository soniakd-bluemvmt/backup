from fastapi import FastAPI
from .models.resource import Base
from .db import engine
from .routers import resource

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(resource.router)
