from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

class ResourceSchema(BaseModel):
    uuid: uuid.UUID
    source_url: str
    unique_name: str
    long_description: str
    create_date: datetime
    json: dict

class FileLoadedSchema(BaseModel):
    uuid: uuid.UUID
    resource_uuid: uuid.UUID
    create_date: datetime
    last_update_date: datetime
    json: dict

class SearchSchema(BaseModel):
    uuid: uuid.UUID
    json: dict
    create_date: datetime
    last_update_date: datetime
    embedding: List[float]
    resource_uuid: uuid.UUID

class Llama2SearchSchema(SearchSchema):
    embedding: List[float]  # still vector but of dim 1024