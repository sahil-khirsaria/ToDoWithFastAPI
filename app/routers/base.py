from fastapi import APIRouter

from app import user_router

api_router = APIRouter()

api_router.include_router(router=user_router, prefix="/users", tags=["User"])