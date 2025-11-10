import os
import logging
from typing import Literal

import httpx
from fastapi import UploadFile

from src.manager import ENVS
from src.common import http_exception as exc

logger = logging.getLogger(__name__)


def validate_file(file: UploadFile) -> None:
    file_ext: str = os.path.splitext(file.filename)[1]  # type: ignore

    if (file.size) and (file.size > ENVS.VALIDATION.FILE_MAX_SIZE):
        raise exc.MaxFileSizeExceedException(
            data={}, message=f"Max file size is {ENVS.VALIDATION.FILE_MAX_SIZE}"
        )

    if file_ext.lower() not in ENVS.VALIDATION.FILE_ALLOWABLE_EXTENSIONS:
        raise exc.NotAllowedFileExtensionsException(
            data={},
            message=f"Allowable extensions are {ENVS.VALIDATION.FILE_ALLOWABLE_EXTENSIONS}",
        )


async def api_call(
    method: Literal["GET", "POST"],
    url: str,
    headers: dict | None = None,
    json: dict | None = None,
    data: dict | None = None,
    files: dict | None = None,
    params: dict | None = None,
) -> httpx.Response:
    connection_pool_cfg = httpx.Limits(
        max_connections=ENVS.HTTPX.MAX_CONNECTIONS,
        keepalive_expiry=ENVS.HTTPX.KEEPALIVE_EXPIRY_SEC,
        max_keepalive_connections=ENVS.HTTPX.MAX_KEEPALIVE_CONNECTIONS,
    )
    timeout_cfg = httpx.Timeout(
        connect=ENVS.HTTPX.CONNECT_TIMEOUT_SEC,
        read=ENVS.HTTPX.READ_TIMEOUT_SEC,
        write=ENVS.HTTPX.WRITE_TIMEOUT_SEC,
        pool=ENVS.HTTPX.POOL_TIMEOUT_SEC,
    )

    try:
        async with httpx.AsyncClient(
            timeout=timeout_cfg, limits=connection_pool_cfg
        ) as client:
            return await client.request(
                method=method,
                url=url,
                headers=headers,
                json=json,
                data=data,
                files=files,
                params=params,
            )

    except httpx.TimeoutException as ex:
        logger.critical(ex)
        raise exc.UnexpectedError(data=str(ex))

    except Exception as ex:
        logger.critical(ex)
        raise exc.UnexpectedError(data=str(ex))
