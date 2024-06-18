import csv
from datetime import date
from io import BytesIO, StringIO

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import FileResponse, StreamingResponse

from schemas.history_register_schema import (
    HistoryInstanceResponse,
    HistoryRegisterListResponse,
)
from schemas.token_schema import TokenData
from services.history_register_service import HistoryRegisterService
from utils.paginate import PaginationRequestBodySchema
from utils.security_manager import SecurityManager

router = APIRouter(prefix="/v1/history_register")


@router.get("/list", summary="Список History Register")
async def get_history_register_list_router(
    service: HistoryRegisterService = Depends(),
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
    pagination: PaginationRequestBodySchema = Depends(),
):
    history_registers = await service.get_history_register_list(
        access_token_data=access_token_data, pagination=pagination
    )
    return history_registers


@router.get(
    "/csv",
    summary="Список History Register в csv файл",
    response_class=StreamingResponse,
)
async def get_history_register_list_router(
    date_from: str | date,
    date_to: str | date,
    service: HistoryRegisterService = Depends(),
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
):
    return await service.get_history_csv(
        date_from=date_from, date_to=date_to, access_token_data=access_token_data
    )


@router.get(
    "/{history_register_id}",
    summary="Получить History Register по ID",
    response_model=HistoryInstanceResponse,
)
async def get_history_register_by_id_router(
    history_register_id: int,
    service: HistoryRegisterService = Depends(),
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
):
    history_register = await service.get_history_register_by_id(
        access_token_data=access_token_data, history_register_id=history_register_id
    )
    if not history_register:
        raise HTTPException(
            status_code=404,
            detail=f"History Register с ID {history_register_id} не найден",
        )
    return history_register
