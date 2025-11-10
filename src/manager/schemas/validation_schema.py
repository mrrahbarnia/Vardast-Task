from pydantic_settings import BaseSettings, SettingsConfigDict


class ValidationSchema(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="VALIDATION__")

    FILE_MAX_SIZE: int
    FILE_ALLOWABLE_EXTENSIONS: list[str]
