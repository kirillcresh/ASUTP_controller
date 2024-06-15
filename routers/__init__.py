from fastapi import APIRouter

from routers import auth_router

router = APIRouter()

router.include_router(auth_router.router, tags=["Auth"])
