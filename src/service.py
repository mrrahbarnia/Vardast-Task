import logging
import hashlib

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.common import types, http_exception as exc
from src.common.utils import validate_file
from src.interface import IRepository

logger = logging.getLogger(__name__)


class Service:
    def __init__(
        self, repository: IRepository, session_maker: async_sessionmaker[AsyncSession]
    ) -> None:
        self._transaction = session_maker
        self._repo = repository

    def mock_embed(self, text: str) -> list[float]:
        # I dont have OpenAI API key so i decided to use LLM code for mock_embed :)
        h = hashlib.sha256(text.encode()).digest()
        vec = [((b % 128) - 64) / 64.0 for b in h[:32]]  # 32-dim vector
        return vec

    def chunk_files_content(self, text: str, max_chars: int = 500) -> list[str]:
        chunks: list[str] = []
        current: list[str] = []
        current_len = 0

        for paragraph in text.split("\n"):
            if current_len + len(paragraph) > max_chars:
                chunks.append(" ".join(current))
                current = []
                current_len = 0
            current.append(paragraph)
            current_len += len(paragraph)
        if current:
            chunks.append(" ".join(current))
        return chunks

    async def read_file_contents(self, files: list[UploadFile]) -> None:
        try:
            inserting_values: list[types.DocumentTypedDict] = []
            for file in files:
                validate_file(file)
                content = (await file.read()).decode("utf-8") + "\n"
                # I converted entire file contents into some chunks for preventing irrelevant noise
                chunks = self.chunk_files_content(content)
                inserting_values.extend(
                    {"chunk": chunk, "embedding": self.mock_embed(chunk)}
                    for chunk in chunks
                )

            if len(inserting_values) > 0:
                async with self._transaction.begin() as tx:
                    await self._repo.bulk_create_documents(
                        values=inserting_values, session=tx
                    )

        except (
            exc.MaxFileSizeExceedException,
            exc.NotAllowedFileExtensionsException,
        ) as ex:
            logger.info(ex)
            raise

        except Exception as ex:
            logger.critical(ex)
            raise exc.UnexpectedError(data=str(ex))
