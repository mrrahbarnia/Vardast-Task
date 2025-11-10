from functools import lru_cache

from src.models import SESSION_MAKER
from src.repository import PostgresRepository


@lru_cache
def get_session_maker():
    return SESSION_MAKER


@lru_cache
def get_repo():
    return PostgresRepository()
