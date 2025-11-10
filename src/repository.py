from typing import Sequence

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import types
from src.models import Document


class PostgresRepository:
    async def bulk_create_documents(
        self, values: list[types.DocumentTypedDict], session: AsyncSession
    ) -> None:
        stmt = sa.insert(Document).values(values)
        await session.execute(stmt)

    async def search_similar_documents(
        self, query_vector: list[float], limit: int, session: AsyncSession
    ) -> Sequence[Document]:
        stmt = (
            sa.select(Document)
            .order_by(Document.embedding.cosine_distance(query_vector))
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
