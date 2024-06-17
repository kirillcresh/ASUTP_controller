from fastapi import APIRouter, Depends, HTTPException

from schemas.param_schema import ParamListResponse
from schemas.token_schema import GetRefreshData
from services.param_service import ParamService
from utils.paginate import PaginationRequestBodySchema
from utils.security_manager import SecurityManager

router = APIRouter(prefix="/v1/param")


@router.get("/list", summary="Список Param")
async def get_param_list_router(
    service: ParamService = Depends(),
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
    pagination: PaginationRequestBodySchema = Depends(),
):
    params = await service.get_param_list(
        # refresh_data=refresh_data,
        pagination=pagination
    )
    return params


@router.get(
    "/{param_id}",
    summary="Получить Param по ID",
    response_model=ParamListResponse,
)
async def get_param_by_id_router(
    param_id: int,
    service: ParamService = Depends()
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
):
    param = await service.get_param_by_id(
        # refresh_data=refresh_data,
        param_id=param_id
    )
    if not param:
        raise HTTPException(
            status_code=404, detail=f"Param с ID {param_id} не найден"
        )
    return param
