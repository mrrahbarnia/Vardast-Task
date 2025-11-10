from typing import Any

from fastapi import HTTPException, status

from src.manager import ENVS
from src.common.types import ENVIRONMENT


class AppBaseException(HTTPException):
    def __init__(
        self,
        *,
        message: str,
        success: bool,
        status_code: int,
        data: Any | None = None,
    ):
        if (
            (ENVS.RUN_MODE.ENVIRONMENT == ENVIRONMENT.PRODUCTION.value)
            and (status_code >= 500)
        ):  # In this condition i have decided to not expose any detail about server errors in production environment.
            self.data = None
        else:
            self.data = str(data)

        self.message = message
        self.status_code = status_code
        self.success = success
        super().__init__(status_code=status_code)


class BadRequestException(AppBaseException):
    def __init__(self, data: dict, message: str = "Bad request."):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            success=False,
            data=data,
        )
