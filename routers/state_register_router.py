from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import StreamingResponse

from schemas.state_register_schema import (
    StateInstanceResponse,
    StateRegisterListResponse,
)
from schemas.token_schema import TokenData
from services.state_register_service import StateRegisterService
from utils.paginate import PaginationRequestBodySchema
from utils.security_manager import SecurityManager

router = APIRouter(prefix="/v1/stare_register")


@router.get("/list", summary="Список State Register")
async def get_state_register_list_router(
    service: StateRegisterService = Depends(),
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
    pagination: PaginationRequestBodySchema = Depends(),
):
    states = await service.get_state_register_list(
        access_token_data=access_token_data, pagination=pagination
    )
    return states


@router.get(
    "/csv", summary="Список State Register в csv файл", response_class=StreamingResponse
)
async def get_history_register_list_router(
    date_from: str | date,
    date_to: str | date,
    service: StateRegisterService = Depends(),
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
):
    return await service.get_state_csv(
        date_from=date_from, date_to=date_to, access_token_data=access_token_data
    )


@router.get(
    "/{state_id}",
    summary="Получить State Register по ID",
    response_model=StateInstanceResponse,
)
async def get_state_register_by_id_router(
    state_id: int,
    service: StateRegisterService = Depends(),
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
):
    state = await service.get_state_register_by_id(
        access_token_data=access_token_data, state_register_id=state_id
    )
    if not state:
        raise HTTPException(
            status_code=404, detail=f"State Register с ID {state_id} не найден"
        )
    return state
