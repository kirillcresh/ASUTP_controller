from fastapi import Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from loggers.handler import exception_handler
from loggers.logger import (
    get_custom_logger,
    get_rotating_file_handler,
    logger_decorator,
)
from models.action_model import Action
from models.maintenance_journal_model import MaintenanceJournal
from models.user_model import User
from schemas.maintenance_schema import MaintenanceBodySchema, MaintenanceResponse
from schemas.token_schema import TokenData
from services import CommonResource
from settings import settings
from utils.paginate import PaginationRequestBodySchema, paginate

logger = get_custom_logger(
    logger_name=__name__,
    handlers=[
        get_rotating_file_handler(settings.PATH_LOG_DIR, "maintenance_service.log")
    ],
)


class MaintenanceService(CommonResource):
    class Config:
        decorators = [logger_decorator(logger), exception_handler(logger)]

    async def create_maintenance(
        self, data_dct: MaintenanceBodySchema, access_token_data: TokenData
    ):
        user = (
            await self.session.execute(
                select(User).where(User.id == data_dct.created_by)
            )
        ).scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с id = {data_dct.created_by} не найден.",
            )

        action = (
            await self.session.execute(
                select(Action).where(Action.id == data_dct.action_id)
            )
        ).scalar_one_or_none()
        if not action:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Действие с id = {data_dct.action_id} не найдено",
            )
        maintenance = (
            await self.session.execute(
                insert(MaintenanceJournal)
                .values(**data_dct.dict())
                .returning(MaintenanceJournal)
            )
        ).scalar_one_or_none()
        await self.session.commit()
        return maintenance

    async def get_list_maintenance(
        self, access_token_data: TokenData, pagination: PaginationRequestBodySchema
    ):
        maintenances = await super().get_list(model=MaintenanceJournal)
        return paginate(
            data=maintenances, dto=pagination, data_schema=MaintenanceResponse
        )

    async def get_maintenance_by_id(
        self, access_token_data: TokenData, maintenance_id: int
    ):
        return await super().get_by_id(
            model=MaintenanceJournal, object_id=maintenance_id
        )

    async def delete_maintenance(
        self, access_token_data: TokenData, maintenance_id: int
    ):
        await super().delete(model=MaintenanceJournal, object_id=maintenance_id)

    async def update_maintenance(
        self,
        access_token_data: TokenData,
        maintenance_id: int,
        data_dct: MaintenanceBodySchema,
    ):
        await super().update(
            model=MaintenanceJournal, object_id=maintenance_id, **data_dct.dict()
        )

    async def partial_update_maintenance(
        self, access_token_data: TokenData, maintenance_id: int, fields: dict
    ):
        await super().partial_update(
            model=MaintenanceJournal, object_id=maintenance_id, fields=fields
        )
