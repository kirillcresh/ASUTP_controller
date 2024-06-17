from fastapi import APIRouter, Depends, HTTPException

from schemas.param_schema import ParamListResponse
from schemas.token_schema import TokenData
from services.param_service import ParamService
from utils.paginate import PaginationRequestBodySchema
from utils.security_manager import SecurityManager

router = APIRouter(prefix="/v1/param")


@router.get("/list", summary="Список Param")
async def get_param_list_router(
    service: ParamService = Depends(),
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
    pagination: PaginationRequestBodySchema = Depends(),
):
    params = await service.get_param_list(
        access_token_data=access_token_data,
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
    service: ParamService = Depends(),
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
):
    param = await service.get_param_by_id(
        access_token_data=access_token_data,
        param_id=param_id
    )
    if not param:
        raise HTTPException(
            status_code=404, detail=f"Param с ID {param_id} не найден"
        )
    return param
