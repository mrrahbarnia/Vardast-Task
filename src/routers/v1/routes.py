from typing import Annotated

from fastapi import APIRouter, UploadFile, status, Depends, File, Query
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.common.http_response import AppResponse
from src.service import Service
from src.dependencies import get_session_maker, get_repo
from src.repository import PostgresRepository
from src.schemas import AskIn, AskFilterQuery

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


@router.post(
    "/ask",
    status_code=status.HTTP_200_OK,
)
async def ask(
    payload: AskIn,
    filter_query: Annotated[AskFilterQuery, Query()],
    session_maker: Annotated[
        async_sessionmaker[AsyncSession], Depends(get_session_maker)
    ],
    repo: Annotated[PostgresRepository, Depends(get_repo)],
):
    response = await Service(repository=repo, session_maker=session_maker).ask(
        dto=payload, filter_query=filter_query
    )
    return response
