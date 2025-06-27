from pydantic import BaseModel, Field
from typing import List
import uuid
from enum import Enum

class ResourceType(str, Enum):
    SIDECAR = "SIDECAR"
    DATASOURCE = "DATASOURCE"
    DATABOOK = "DATABOOK"

class ResourceCreate(BaseModel):
    resource_uuid: uuid.UUID
    tenant_uuid: uuid.UUID
    resource_type: ResourceType
    resource_name: str
    resource_description: str | None = None
    text: str = Field(description="Text to be embedded and stored")

class ResourceRead(BaseModel):
    resource_uuid: uuid.UUID
    resource_name: str
    resource_description: str | None
    resource_type: ResourceType
    score: float

class ResourceUpdate(BaseModel):
    resource_name: str | None = None
    resource_description: str | None = None
    text: str | None = None  # if present, re-embed
