from fastapi import APIRouter, Depends, HTTPException

from schemas.error_schema import ErrorListResponse
from schemas.token_schema import TokenData
from services.error_service import ErrorService
from utils.paginate import PaginationRequestBodySchema
from utils.security_manager import SecurityManager

router = APIRouter(prefix="/v1/error")


@router.get("/list", summary="Список Error")
async def get_error_list_router(
    service: ErrorService = Depends(),
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
    pagination: PaginationRequestBodySchema = Depends(),
):
    errors = await service.get_error_list(
        access_token_data=access_token_data,
        pagination=pagination
    )
    return errors


@router.get(
    "/{error_id}", summary="Получить Error по ID", response_model=ErrorListResponse
)
async def get_error_by_id_router(
    error_id: int,
    service: ErrorService = Depends(),
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
):
    error = await service.get_error_by_id(
        access_token_data=access_token_data,
        error_id=error_id
    )
    if not error:
        raise HTTPException(status_code=404, detail=f"Error с ID {error_id} не найден")
    return error
