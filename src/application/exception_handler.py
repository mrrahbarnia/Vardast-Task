from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.common.http_exception import AppBaseException


async def app_base_exception_handler(request: Request, exc: AppBaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": exc.success,
            "status_code": exc.status_code,
            "message": exc.message,
            "data": exc.data,
        },
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(AppBaseException, app_base_exception_handler)  # type: ignore
