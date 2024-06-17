from fastapi import APIRouter, Depends, HTTPException

from schemas.history_register_schema import HistoryRegisterListResponse
from schemas.token_schema import GetRefreshData
from services.history_register_service import HistoryRegisterService
from utils.paginate import PaginationRequestBodySchema
from utils.security_manager import SecurityManager

router = APIRouter(prefix="/v1/history_register")


@router.get("/list", summary="Список History Register")
async def get_history_register_list_router(
    service: HistoryRegisterService = Depends(),
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
    pagination: PaginationRequestBodySchema = Depends(),
):
    history_registers = await service.get_history_register_list(
        # refresh_data=refresh_data,
        pagination=pagination
    )
    return history_registers


@router.get(
    "/{history_register_id}",
    summary="Получить History Register по ID",
    response_model=HistoryRegisterListResponse,
)
async def get_history_register_by_id_router(
    history_register_id: int,
    service: HistoryRegisterService = Depends()
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
):
    history_register = await service.get_history_register_by_id(
        # refresh_data=refresh_data,
        history_register_id=history_register_id
    )
    if not history_register:
        raise HTTPException(
            status_code=404,
            detail=f"History Register с ID {history_register_id} не найден",
        )
    return history_register