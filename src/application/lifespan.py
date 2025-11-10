import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from logging.config import dictConfig

from fastapi import FastAPI

from src.application.logger import LogConfig


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # ============================== On startup
    logger.info("Logger is running...")
    try:
        dictConfig(LogConfig().model_dump())
    except Exception as ex:
        print(f"Logger doesnt starts successfully due to : {ex}")
        raise RuntimeError("Logger doesnt starts successfully")

    logger.info("Application is running...")
    yield
    # ============================== On shutdown

    logger.info("Application is shutting down...")
