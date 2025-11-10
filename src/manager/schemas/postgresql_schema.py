from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresqlSchema(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRESQL__")

    USERNAME: str
    PASSWORD: str
    DATABASE: str
    PORT: str
    HOST: str
