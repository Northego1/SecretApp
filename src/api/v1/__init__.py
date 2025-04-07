from fastapi import APIRouter

from api.v1.secret_api import router as secret_router

union_router = APIRouter(prefix="/api/v1")

union_router.include_router(secret_router)
