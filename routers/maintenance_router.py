from fastapi import APIRouter, Depends, Body

from schemas.maintenance_schema import MaintenanceBodySchema
from schemas.token_schema import TokenData
from services.maintenance_service import MaintenanceService
from utils.paginate import PaginationRequestBodySchema
from utils.security_manager import SecurityManager

router = APIRouter(prefix="/v1/maintenance")


@router.post(
    "/maintenance", summary="Создание записи в журнале обслуживания"
)
async def create_maintenance(
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
    service: MaintenanceService = Depends(),
    data_dct: MaintenanceBodySchema = Body(),
):
    return await service.create_maintenance(data_dct=data_dct, access_token_data=access_token_data)


@router.get("/maintenance/all", summary="Получение журнала обслуживания")
async def get_list_maintenance(
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
    service: MaintenanceService = Depends(),
    pagination: PaginationRequestBodySchema = Depends(),
):
    return await service.get_list_maintenance(access_token_data=access_token_data, pagination=pagination)