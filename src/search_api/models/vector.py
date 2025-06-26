from sqlalchemy import Text, TIMESTAMP, ForeignKey, JSON, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
import uuid

class Base(DeclarativeBase):
    pass

class Resource(Base):
    __tablename__ = "resources"

    uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    source_url: Mapped[str] = mapped_column(VARCHAR(512))
    unique_name: Mapped[str] = mapped_column(VARCHAR(512), unique=True)
    long_description: Mapped[str] = mapped_column(Text)
    create_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    json: Mapped[dict] = mapped_column(JSON, nullable=False)

    files_loaded = relationship("FileLoaded", back_populates="resource")

class FileLoaded(Base):
    __tablename__ = "files_loaded"

    uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    resource_uuid: Mapped[uuid.UUID] = mapped_column(ForeignKey("resources.uuid"))
    create_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    last_update_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    json: Mapped[dict] = mapped_column(JSON, nullable=False)

    resource = relationship("Resource", back_populates="files_loaded")

class Search(Base):
    __tablename__ = "searches"

    uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    json: Mapped[dict] = mapped_column(JSON, nullable=False)
    create_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    last_update_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536))
    resource_uuid: Mapped[uuid.UUID] = mapped_column()

class Llama2Search(Base):
    __tablename__ = "llama2_searches"

    uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    json: Mapped[dict] = mapped_column(JSON, nullable=False)
    create_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    last_update_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(1024))
    resource_uuid: Mapped[uuid.UUID] = mapped_column()