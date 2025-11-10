from fastapi import FastAPI

from src.manager import ENVS
from src.common.types import ENVIRONMENT
from src.application.lifespan import lifespan


app: FastAPI = FastAPI(
    title=ENVS.FASTAPI.APPLICATION_NAME,
    description=ENVS.FASTAPI.APPLICATION_DESCRIPTION,
    version=ENVS.FASTAPI.APPLICATION_VERSION,
    docs_url=None
    if ENVS.RUN_MODE.ENVIRONMENT == ENVIRONMENT.PRODUCTION.value
    else ENVS.FASTAPI.DOCS_URL,
    openapi_url=None
    if ENVS.RUN_MODE.ENVIRONMENT == ENVIRONMENT.PRODUCTION.value
    else ENVS.FASTAPI.OPENAPI_URL,
    redoc_url=None
    if ENVS.RUN_MODE.ENVIRONMENT == ENVIRONMENT.PRODUCTION.value
    else ENVS.FASTAPI.REDOC_URL,
    lifespan=lifespan,
)
