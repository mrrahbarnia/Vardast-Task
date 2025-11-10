from fastapi import APIRouter

router = APIRouter(prefix="/v1")


@router.get("/healthcheck")
async def health_check():
    return "OK"
