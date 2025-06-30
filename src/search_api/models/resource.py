from sqlalchemy import Column, Enum, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector
import uuid
import enum

Base = declarative_base()


class ResourceType(str, enum.Enum):
    SIDECAR = "SIDECAR"
    DATASOURCE = "DATASOURCE"
    DATABOOK = "DATABOOK"


class Resource(Base):
    __tablename__ = "resources"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_uuid = Column(UUID(as_uuid=True), nullable=False)
    tenant_uuid = Column(UUID(as_uuid=True), nullable=False)
    resource_type = Column(Enum(ResourceType, name="resourcetype"), nullable=False)
    resource_name = Column(String(255), nullable=False)
    resource_description = Column(Text, nullable=True)
    embedding = Column(Vector(384), nullable=False)  # adjust dimension based on model used
