from functools import lru_cache

from pydantic import BaseModel

from src.manager import schemas


class _ENVS(BaseModel):
    RUN_MODE: schemas.RunModeSchema = schemas.RunModeSchema()  # type: ignore
    UVICORN: schemas.UvicornSchema = schemas.UvicornSchema()  # type: ignore
    FASTAPI: schemas.FastAPISchema = schemas.FastAPISchema()  # type: ignore


@lru_cache
def get_envs() -> _ENVS:
    return _ENVS()  # type: ignore


ENVS = get_envs()
