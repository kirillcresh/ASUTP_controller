from fastapi import APIRouter, Depends, HTTPException

from schemas.error_schema import ErrorListResponse
from schemas.token_schema import GetRefreshData
from services.error_service import ErrorService
from utils.paginate import PaginationRequestBodySchema
from utils.security_manager import SecurityManager

router = APIRouter(prefix="/v1/error")


@router.get("/list", summary="Список Error")
async def get_error_list_router(
    service: ErrorService = Depends(),
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
    pagination: PaginationRequestBodySchema = Depends(),
):
    errors = await service.get_error_list(
        # refresh_data=refresh_data,
        pagination=pagination
    )
    return errors


@router.get(
    "/{error_id}", summary="Получить Error по ID", response_model=ErrorListResponse
)
async def get_element_by_id_router(
    error_id: int,
    service: ErrorService = Depends()
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
):
    error = await service.get_error_by_id(
        # refresh_data=refresh_data,
        action_id=error_id
    )
    if not error:
        raise HTTPException(
            status_code=404, detail=f"Element с ID {error_id} не найден"
        )
    return error
