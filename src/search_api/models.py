import enum
import uuid
from sqlalchemy import (
    Column,
    Enum,
    String,
    Text,
    LargeBinary,
)
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ResourceTypeEnum(str, enum.Enum):
    SIDECAR = "SIDECAR"
    DATASOURCE = "DATASOURCE"
    DATABOOK = "DATABOOK"


class Resource(Base):
    __tablename__ = "resources"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_uuid = Column(UUID(as_uuid=True), nullable=False)
    resource_type = Column(Enum(ResourceTypeEnum, name="resourcetype"), nullable=False)
    resource_name = Column(String(255), nullable=False)
    resource_description = Column(Text, nullable=True)
    embedding = Column(BYTEA, nullable=True)  # or use LargeBinary if not using BYTEA
