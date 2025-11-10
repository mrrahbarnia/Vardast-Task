from pydantic_settings import BaseSettings, SettingsConfigDict

from src.common.types import ENVIRONMENT


class RunModeSchema(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RUN_MODE__")

    ENVIRONMENT: ENVIRONMENT
