from fastapi import APIRouter

from src.routers import v1_router

router = APIRouter()

# ================ Including application routers here ================ #
router.include_router(v1_router)
