import os

from fastapi import UploadFile

from src.manager import ENVS
from src.common import http_exception as exc


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
