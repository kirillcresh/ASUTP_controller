from fastapi import APIRouter

from routers import (
    action_router,
    auth_router,
    current_state_router,
    element_router,
    error_router,
    history_register_router,
    maintenance_router,
    param_router,
    report_router,
    state_register_router,
    user_router,
)

router = APIRouter()

router.include_router(auth_router.router, tags=["Auth"])
router.include_router(maintenance_router.router, tags=["Maintenance Journal"])
router.include_router(action_router.router, tags=["Action"])
router.include_router(current_state_router.router, tags=["Current State"])
router.include_router(element_router.router, tags=["Element"])
router.include_router(error_router.router, tags=["Error"])
router.include_router(history_register_router.router, tags=["History Register"])
router.include_router(param_router.router, tags=["Param"])
router.include_router(report_router.router, tags=["Report"])
router.include_router(state_register_router.router, tags=["State Register"])
router.include_router(user_router.router, tags=["User"])
