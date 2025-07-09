import enum
import uuid
from sqlalchemy import Column, Enum, String, Text, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

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

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_uuid = Column(UUID(as_uuid=True), nullable=False)
    tenant_uuid = Column(UUID(as_uuid=True), nullable=False)  # required for tenant filtering
    resource_type = Column(Enum(ResourceType, name="resourcetype"), nullable=False)
    resource_name = Column(String(255), nullable=False)
    resource_description = Column(Text, nullable=True)
    embedding = Column(Vector(), nullable=True)  # vector column for pgvector
    embedding_status = Column(Enum(EmbeddingStatus, name="embeddingstatus"), default=EmbeddingStatus.PENDING)
    status_detail = Column(Text, nullable=True)