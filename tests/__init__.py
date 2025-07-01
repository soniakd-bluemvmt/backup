from search_api.models import Resource  # if Resource is here
from search_api.schemas import ResourceType, EmbeddingStatus  # if these are here

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
