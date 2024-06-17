from fastapi import APIRouter, Depends, HTTPException

from schemas.current_state_schema import CurrentStateListResponse
from schemas.token_schema import GetRefreshData
from services.current_state_service import CurrentStateService
from utils.paginate import PaginationRequestBodySchema
from utils.security_manager import SecurityManager

router = APIRouter(prefix="/v1/current_state")


@router.get("/list", summary="Список Current State")
async def get_state_router(
    service: CurrentStateService = Depends(),
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
    pagination: PaginationRequestBodySchema = Depends(),
):
    actions = await service.get_state_list(
        # refresh_data=refresh_data,
        pagination=pagination
    )
    return actions


@router.get(
    "/{state_id}", summary="Получить Current State по ID", response_model=CurrentStateListResponse
)
async def get_state_by_id(
    state_id: int,
    service: CurrentStateService = Depends()
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
):
    state = await service.get_state_by_id(
        # refresh_data=refresh_data,
        action_id=state_id
    )
    if not state:
        raise HTTPException(
            status_code=404, detail=f"Current state с ID {state_id} не найден"
        )
    return state