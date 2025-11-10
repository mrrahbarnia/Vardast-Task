from pydantic_settings import BaseSettings, SettingsConfigDict


class FastAPISchema(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="FASTAPI__")

    APPLICATION_NAME: str
    APPLICATION_DESCRIPTION: str
    APPLICATION_VERSION: str
    DOCS_URL: str
    OPENAPI_URL: str
    REDOC_URL: str
    ENDPOINT_PREFIX: str
