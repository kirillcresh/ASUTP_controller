from fastapi import APIRouter, Depends, HTTPException

from schemas.action_schema import ActionListResponse
from schemas.token_schema import GetRefreshData
from services.action_service import ActionService
from utils.paginate import PaginationRequestBodySchema
from utils.security_manager import SecurityManager

router = APIRouter(prefix="/v1/action")


@router.get("/list", summary="Список Action")
async def get_list_router(
    service: ActionService = Depends(),
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
    pagination: PaginationRequestBodySchema = Depends(),
):
    actions = await service.get_action_list(
        # refresh_data=refresh_data,
        pagination=pagination
    )
    return actions


@router.get("/list", summary="Список Action")
async def get_list_router(
    service: ActionService = Depends(),
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
    pagination: PaginationRequestBodySchema = Depends(),
):
    actions = await service.get_action_list(
        # refresh_data=refresh_data,
        pagination=pagination
    )
    return actions


@router.get(
    "/{action_id}", summary="Получить Action по ID", response_model=ActionListResponse
)
async def get_action_by_id(
    action_id: int,
    service: ActionService = Depends()
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
):
    action = await service.get_action_by_id(
        # refresh_data=refresh_data,
        action_id=action_id
    )
    if not action:
        raise HTTPException(
            status_code=404, detail=f"Action с ID {action_id} не найден"
        )
    return action
