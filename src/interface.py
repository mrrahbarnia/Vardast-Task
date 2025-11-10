from typing import Protocol, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.common import types
from src.models import Document


class IRepository(Protocol):
    async def bulk_create_documents(
        self, values: list[types.DocumentTypedDict], session: AsyncSession
    ) -> None: ...

    async def search_similar_documents(
        self, query_vector: list[float], limit: int, session: AsyncSession
    ) -> Sequence[Document]: ...
