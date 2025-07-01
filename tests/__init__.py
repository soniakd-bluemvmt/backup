from search_api.models import Resource  # if Resource is here
from search_api.schemas.resource import Resource, ResourceType, EmbeddingStatus
from sqlalchemy.orm import declarative_base


Base = declarative_base()
