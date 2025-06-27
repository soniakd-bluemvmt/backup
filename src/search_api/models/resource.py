from sqlalchemy import Text, TIMESTAMP, JSON, VARCHAR, Enum as PgEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pgvector.sqlalchemy import Vector
import uuid
import enum

class Base(DeclarativeBase):
    pass

class ResourceType(str, enum.Enum):
    SIDECAR = "SIDECAR"
    DATASOURCE = "DATASOURCE"
    DATABOOK = "DATABOOK"

class Resource(Base):
    __tablename__ = "resources"

    uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    resource_uuid: Mapped[uuid.UUID] = mapped_column(nullable=False, unique=True)
    resource_type: Mapped[ResourceType] = mapped_column(PgEnum(ResourceType), nullable=False)
    resource_name: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    resource_description: Mapped[str] = mapped_column(Text, nullable=True)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536), nullable=False)