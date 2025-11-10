from datetime import datetime
from uuid import uuid4

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    create_async_engine,
)
from pgvector.sqlalchemy import Vector  # type: ignore

from src.manager import ENVS
from src.common import types

POSTGRES_DSN = f"postgresql+asyncpg://{ENVS.POSTGRESQL.USERNAME}:{ENVS.POSTGRESQL.PASSWORD}@{ENVS.POSTGRESQL.HOST}:{ENVS.POSTGRESQL.PORT}/{ENVS.POSTGRESQL.DATABASE}"

ASYNC_ENGINE: AsyncEngine = create_async_engine(POSTGRES_DSN)
SESSION_MAKER = async_sessionmaker(ASYNC_ENGINE, expire_on_commit=False)


class BaseModel(so.DeclarativeBase, so.MappedAsDataclass):
    type_annotation_map = {
        datetime: sa.types.TIMESTAMP(timezone=True),
    }


class Document(BaseModel):
    __tablename__ = "documents"
    chunk: so.Mapped[str] = so.mapped_column(sa.String)
    embedding: so.Mapped[list[float]] = so.mapped_column(Vector(32))
    id: so.Mapped[types.DocumentId] = so.mapped_column(
        primary_key=True, default=lambda: uuid4()
    )
