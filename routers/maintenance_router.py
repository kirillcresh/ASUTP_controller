from fastapi import APIRouter, Body, Depends, HTTPException

from schemas.maintenance_schema import MaintenanceBodySchema
from schemas.token_schema import TokenData
from services.maintenance_service import MaintenanceService
from utils.paginate import PaginationRequestBodySchema
from utils.security_manager import SecurityManager

router = APIRouter(prefix="/v1/maintenance")


@router.post("/maintenance", summary="Создание записи в журнале обслуживания")
async def create_maintenance(
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
    service: MaintenanceService = Depends(),
    data_dct: MaintenanceBodySchema = Body(),
):
    return await service.create_maintenance(
        data_dct=data_dct, access_token_data=access_token_data
    )


@router.get("/maintenance/all", summary="Получение журнала обслуживания")
async def get_list_maintenance(
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
    service: MaintenanceService = Depends(),
    pagination: PaginationRequestBodySchema = Depends(),
):
    return await service.get_list_maintenance(
        access_token_data=access_token_data,
        pagination=pagination
    )


@router.get("/maintenance/{maintenance_id}", summary="Получение записи в журнале обслуживания")
async def get_maintenance_by_id(
    maintenance_id: int,
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
    service: MaintenanceService = Depends(),
):
    maintence = await service.get_maintenance_by_id(
        access_token_data=access_token_data,
        maintenance_id=maintenance_id
    )
    if not maintence:
        raise HTTPException(
            status_code=404, detail=f"Maintenance с ID {maintenance_id} не найден"
        )
    return await service.get_maintenance_by_id(access_token_data=access_token_data, maintenance_id=maintenance_id)


@router.delete("/maintenance/{maintenance_id}", summary="Удаление записи в журнале обслуживания", status_code=204)
async def delete_maintenance(
    maintenance_id: int,
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
    service: MaintenanceService = Depends(),
):
    maintence = await service.get_maintenance_by_id(
        access_token_data=access_token_data,
        maintenance_id=maintenance_id
    )
    if not maintence:
        raise HTTPException(
            status_code=404, detail=f"Maintenance с ID {maintenance_id} не найден"
        )
    await service.delete_maintenance(access_token_data=access_token_data, maintenance_id=maintenance_id)


@router.put("/maintenance/{maintenance_id}", summary="Обновление записи в журнале обслуживания")
async def update_maintenance(
    maintenance_id: int,
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
    service: MaintenanceService = Depends(),
    data_dct: MaintenanceBodySchema = Body(),
):
    maintence = await service.get_maintenance_by_id(
        access_token_data=access_token_data,
        maintenance_id=maintenance_id
    )
    if not maintence:
        raise HTTPException(
            status_code=404, detail=f"Maintenance с ID {maintenance_id} не найден"
        )
    await service.update_maintenance(
        access_token_data=access_token_data,
        maintenance_id=maintenance_id,
        data_dct=data_dct
    )
    maintence = await service.get_maintenance_by_id(access_token_data=access_token_data, maintenance_id=maintenance_id)
    return maintence


@router.patch("/maintenance/{maintenance_id}", summary="Обновление записи в журнале обслуживания")
async def update_maintenance(
    maintenance_id: int,
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
    service: MaintenanceService = Depends(),
    data_dct: MaintenanceBodySchema = Body(),
):
    maintence = await service.get_maintenance_by_id(
        access_token_data=access_token_data,
        maintenance_id=maintenance_id
    )
    if not maintence:
        raise HTTPException(
            status_code=404, detail=f"Maintenance с ID {maintenance_id} не найден"
        )
    await service.update_maintenance(
        access_token_data=access_token_data,
        maintenance_id=maintenance_id,
        data_dct=data_dct
    )
    maintence = await service.get_maintenance_by_id(
        access_token_data=access_token_data,
        maintenance_id=maintenance_id)
    return maintence
