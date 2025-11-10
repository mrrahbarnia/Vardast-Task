from pydantic_settings import BaseSettings, SettingsConfigDict


class UvicornSchema(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="UVICORN__")

    HOST: str
    PORT: int
    LOG_LEVEL: str
    PROXY_HEADERS: bool
    FORWARDED_ALLOW_IPS: str
    WORKERS: int
    SERVER_HEADER: bool
