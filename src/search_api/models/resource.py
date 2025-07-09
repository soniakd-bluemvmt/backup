from sqlalchemy import Column, String, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import declarative_base
import enum
from sqlalchemy import ForeignKey


Base = declarative_base()

class EmbeddingStatus(enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class ResourceType(enum.Enum):
    SIDECAR = "SIDECAR"
    DATASOURCE = "DATASOURCE"
    DATABOOK = "DATABOOK"

class Resource(Base):
    __tablename__ = "resources"

    resource_uuid = Column(UUID(as_uuid=True), primary_key=True)
    tenant_uuid = Column(UUID(as_uuid=True), nullable=False)
    resource_type = Column(Enum(ResourceType), nullable=False)
    resource_name = Column(String, nullable=False)
    resource_description = Column(String, nullable=True)
    embedding = Column(Vector(1536), nullable=True)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    embedding_status = Column(Enum(EmbeddingStatus), default=EmbeddingStatus.PENDING, nullable=False)
    status_detail = Column(Text, nullable=True)
