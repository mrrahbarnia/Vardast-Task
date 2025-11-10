from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from src.common import types


class IRepository(Protocol):
    async def bulk_create_documents(
        self, values: list[types.DocumentTypedDict], session: AsyncSession
    ) -> None: ...
