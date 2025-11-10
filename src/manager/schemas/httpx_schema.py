from pydantic_settings import BaseSettings, SettingsConfigDict


class HTTPXSchema(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HTTPX__")

    # HTTPX connection pool
    MAX_CONNECTIONS: int
    MAX_KEEPALIVE_CONNECTIONS: int
    KEEPALIVE_EXPIRY_SEC: int

    # HTTPX connection timeout
    CONNECT_TIMEOUT_SEC: float
    READ_TIMEOUT_SEC: float
    WRITE_TIMEOUT_SEC: float
    POOL_TIMEOUT_SEC: float
