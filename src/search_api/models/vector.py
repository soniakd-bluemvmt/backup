from sqlalchemy import Integer, String, Float, Text, TIMESTAMP, ForeignKey, JSON, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector
import uuid

class Base(DeclarativeBase):
    pass

class Datasource(Base):
    __tablename__ = "datasources"

    uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    source_url: Mapped[str] = mapped_column(VARCHAR(512))
    unique_name: Mapped[str] = mapped_column(VARCHAR(512), unique=True)
    long_description: Mapped[str] = mapped_column(Text)
    create_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    json: Mapped[dict] = mapped_column(JSON, nullable=False)

    files_loaded = relationship("FileLoaded", back_populates="datasource")

class FileLoaded(Base):
    __tablename__ = "files_loaded"

    uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    datasource_uuid: Mapped[uuid.UUID] = mapped_column(ForeignKey("datasources.uuid"))
    create_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    last_update_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    json: Mapped[dict] = mapped_column(JSON, nullable=False)

    datasource = relationship("Datasource", back_populates="files_loaded")

class Search(Base):
    __tablename__ = "searches"

    uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    json: Mapped[dict] = mapped_column(JSON, nullable=False)
    create_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    last_update_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536))
    datasource_uuid: Mapped[uuid.UUID] = mapped_column()

class Llama2Search(Base):
    __tablename__ = "llama2_searches"

    uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    json: Mapped[dict] = mapped_column(JSON, nullable=False)
    create_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    last_update_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(1024))
    datasource_uuid: Mapped[uuid.UUID] = mapped_column()
