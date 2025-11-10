from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T")


class AppResponse(BaseModel, Generic[T]):
    success: bool
    status_code: int
    message: str
    data: T | None = None
