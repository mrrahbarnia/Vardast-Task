import logging
import hashlib
from datetime import datetime, timezone

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.common import types, http_exception as exc
from src.common.utils import validate_file, api_call
from src.interface import IRepository
from src.schemas import AskIn, AskFilterQuery

logger = logging.getLogger(__name__)

TOOLS = {
    "current time": "get_current_time",
    "time in": "get_current_time",
    "exchange rate": "get_exchange_rate",
    "convert": "get_exchange_rate",
}


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

    def get_current_time(self, tz: str = "UTC") -> str:
        now = datetime.now(timezone.utc)
        if tz.upper() == "UTC":
            return now.strftime("%Y-%m-%d %H:%M:%S UTC")
        return now.strftime("%Y-%m-%d %H:%M:%S") + f" {tz}"

    async def get_exchange_rate(self, base: str, target: str) -> str | None:
        url = f"https://api.exchangerate-api.com/v4/latest/{base.upper()}"
        response = await api_call(method="GET", url=url)
        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", {})
            rate = rates.get(target.upper())
            if rate:
                return f"1 {base.upper()} = {rate:.4f} {target.upper()}"
            return None
        else:
            return None

    def validate_answer(self, answer: str, context: str) -> bool:
        return any(
            word.lower() in context.lower() for word in answer.split() if len(word) > 3
        )

    def mock_generate_answer(self, query: str, context: str) -> str:
        return f"Answer to '{query}' based on context: {context[:200]}..."

    def detect_tool(self, query: str) -> tuple[str, dict] | None:
        query_lower = query.lower()

        if "time" in query_lower:
            tz = "UTC"
            if "in " in query_lower:
                tz = query_lower.split("in ")[-1].strip()
            return ("get_current_time", {"tz": tz})

        if "exchange rate" in query_lower or "convert" in query_lower:
            parts = query.upper().split()
            try:
                base_idx = parts.index("FROM") + 1
                target_idx = parts.index("TO") + 1
                return (
                    "get_exchange_rate",
                    {"base": parts[base_idx], "target": parts[target_idx]},
                )
            except Exception:
                return ("get_exchange_rate", {"base": "USD", "target": "EUR"})

        return None

    async def ask(self, dto: AskIn, filter_query: AskFilterQuery) -> str:
        try:
            tool_info = self.detect_tool(dto.query)
            if tool_info:
                tool_name, params = tool_info
                tool_func = getattr(self, tool_name)
                if callable(tool_func):
                    if tool_name.startswith("get_exchange_rate"):
                        return await tool_func(**params)  # type: ignore
                    return tool_func(**params)  # type: ignore

            query_vec = self.mock_embed(text=dto.query)
            async with self._transaction.begin() as tx:
                result = await self._repo.search_similar_documents(
                    query_vector=query_vec, limit=filter_query.limit, session=tx
                )
            if len(result) == 0:
                return "Sorry, I don’t have enough information to answer that."

            context_chunks = [doc.chunk for doc in result]
            full_context = "\n".join(context_chunks)

            answer_text = self.mock_generate_answer(
                query=dto.query, context=full_context
            )
            if not self.validate_answer(answer=answer_text, context=full_context):
                return "Sorry, I cannot answer this question based on available information."
            return answer_text

        except Exception as ex:
            logger.critical(ex)
            raise exc.UnexpectedError(data=str(ex))
