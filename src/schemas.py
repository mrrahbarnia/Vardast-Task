from pydantic import BaseModel


class AskIn(BaseModel):
    query: str


class AskFilterQuery(BaseModel):
    limit: int
