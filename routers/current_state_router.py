from fastapi import APIRouter, Depends, HTTPException

from schemas.current_state_schema import CurrentStateListResponse
from schemas.token_schema import  TokenData
from services.current_state_service import CurrentStateService
from utils.paginate import PaginationRequestBodySchema
from utils.security_manager import SecurityManager

router = APIRouter(prefix="/v1/current_state")


@router.get("/list", summary="Список Current State")
async def get_state_list_router(
    service: CurrentStateService = Depends(),
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
    pagination: PaginationRequestBodySchema = Depends(),
):
    states = await service.get_state_list(
        access_token_data=access_token_data,
        pagination=pagination
    )
    return states


@router.get(
    "/{state_id}",
    summary="Получить Current State по ID",
    response_model=CurrentStateListResponse,
)
async def get_state_by_id_router(
    state_id: int,
    service: CurrentStateService = Depends(),
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
):
    state = await service.get_state_by_id(
        access_token_data=access_token_data,
        current_state_id=state_id
    )
    if not state:
        raise HTTPException(
            status_code=404, detail=f"Current state с ID {state_id} не найден"
        )
    return state
