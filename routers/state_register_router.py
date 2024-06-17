from fastapi import APIRouter, Depends, HTTPException

from schemas.state_register_schema import StateRegisterListResponse
from schemas.token_schema import GetRefreshData
from services.state_register_service import StateRegisterService
from utils.paginate import PaginationRequestBodySchema
from utils.security_manager import SecurityManager

router = APIRouter(prefix="/v1/stare_register")


@router.get("/list", summary="Список State Register")
async def get_state_register_list_router(
    service: StateRegisterService = Depends(),
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
    pagination: PaginationRequestBodySchema = Depends(),
):
    states = await service.get_state_register_list(
        # refresh_data=refresh_data,
        pagination=pagination
    )
    return states


@router.get(
    "/{state_id}",
    summary="Получить State Register по ID",
    response_model=StateRegisterListResponse,
)
async def get_state_register_by_id_router(
    state_id: int,
    service: StateRegisterService = Depends()
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
):
    state = await service.get_state_register_by_id(
        # refresh_data=refresh_data,
        state_register_id=state_id
    )
    if not state:
        raise HTTPException(
            status_code=404, detail=f"State Register с ID {state_id} не найден"
        )
    return state
