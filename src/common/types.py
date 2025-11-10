from typing import NewType, TypedDict
from uuid import UUID
from enum import StrEnum, auto


DocumentId = NewType("DocumentId", UUID)


class ENVIRONMENT(StrEnum):
    PRODUCTION = auto()
    DEVELOPMENT = auto()


class DocumentTypedDict(TypedDict):
    embedding: list[float]
    chunk: str
