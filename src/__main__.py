from uvicorn import run

from src.manager import ENVS
from src.common.types import ENVIRONMENT


if __name__ == "__main__":
    run(
        app="src.application.init_app:application",
        host=ENVS.UVICORN.HOST,
        port=ENVS.UVICORN.PORT,
        log_level=ENVS.UVICORN.LOG_LEVEL.lower(),
        proxy_headers=ENVS.UVICORN.PROXY_HEADERS,
        forwarded_allow_ips=ENVS.UVICORN.FORWARDED_ALLOW_IPS,
        reload=False
        if ENVS.RUN_MODE.ENVIRONMENT == ENVIRONMENT.PRODUCTION.value
        else True,
        loop="asyncio",
        workers=ENVS.UVICORN.WORKERS,
        server_header=ENVS.UVICORN.SERVER_HEADER,
    )
