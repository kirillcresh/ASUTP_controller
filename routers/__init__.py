from fastapi import APIRouter

from routers import auth_router, maintenance_router

router = APIRouter()

router.include_router(auth_router.router, tags=["Auth"])
router.include_router(maintenance_router.router, tags=["Crud"])
