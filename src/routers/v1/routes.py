from typing import Annotated

from fastapi import APIRouter, UploadFile, status, Depends, File
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.service import Service
from src.dependencies import get_session_maker, get_repo
from src.repository import PostgresRepository
from src.common.http_response import AppResponse

router = APIRouter(prefix="/v1")


@router.get("/healthcheck")
async def health_check():
    return "OK"


@router.post(
    "/ingest", status_code=status.HTTP_201_CREATED, response_model=AppResponse[dict]
)
async def ingest_data(
    session_maker: Annotated[
        async_sessionmaker[AsyncSession], Depends(get_session_maker)
    ],
    repo: Annotated[PostgresRepository, Depends(get_repo)],
    files: Annotated[list[UploadFile], File(...)],
) -> AppResponse[dict]:
    await Service(repository=repo, session_maker=session_maker).read_file_contents(
        files=files
    )
    return AppResponse[dict](
        success=True,
        status_code=status.HTTP_201_CREATED,
        message="Files content embeded successfully.",
    )
