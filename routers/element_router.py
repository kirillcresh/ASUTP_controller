from fastapi import APIRouter, Depends, HTTPException

from schemas.element_schema import ElementListResponse
from schemas.token_schema import GetRefreshData
from services.element_service import ElementService
from utils.paginate import PaginationRequestBodySchema
from utils.security_manager import SecurityManager

router = APIRouter(prefix="/v1/element")


@router.get("/list", summary="Список Element")
async def get_element_list_router(
    service: ElementService = Depends(),
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
    pagination: PaginationRequestBodySchema = Depends(),
):
    elements = await service.get_element_list(
        # refresh_data=refresh_data,
        pagination=pagination
    )
    return elements


@router.get(
    "/{element_id}",
    summary="Получить Element по ID",
    response_model=ElementListResponse,
)
async def get_element_by_id_router(
    element_id: int,
    service: ElementService = Depends()
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
):
    element = await service.get_element_by_id(
        # refresh_data=refresh_data,
        element_id=element_id
    )
    if not element:
        raise HTTPException(
            status_code=404, detail=f"Element с ID {element_id} не найден"
        )
    return element
