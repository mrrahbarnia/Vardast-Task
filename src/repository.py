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
