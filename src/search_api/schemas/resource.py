from pydantic import BaseModel, UUID4
from enum import Enum
from typing import Optional


class ResourceType(str, Enum):
    SIDECAR = "SIDECAR"
    DATASOURCE = "DATASOURCE"
    DATABOOK = "DATABOOK"


class ResourceCreate(BaseModel):
    resource_uuid: UUID4
    resource_type: ResourceType
    resource_name: str
    resource_description: Optional[str] = None


class ResourceSearchResult(BaseModel):
    resource_uuid: UUID4
    resource_name: str
    resource_description: Optional[str]
    resource_type: ResourceType
    score: float

class EmbeddingStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED" 

class Resource(ResourceSearchResult):
    embedding: Optional[list[float]]
    embedding_status: EmbeddingStatus
    status_detail: Optional[str]

