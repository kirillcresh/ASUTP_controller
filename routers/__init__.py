from fastapi import APIRouter

from routers import action_router, auth_router, current_state_router, maintenance_router

router = APIRouter()

router.include_router(auth_router.router, tags=["Auth"])
router.include_router(maintenance_router.router, tags=["Crud"])
router.include_router(action_router.router, tags=["Action"])
router.include_router(current_state_router.router, tags=["Current State"])
