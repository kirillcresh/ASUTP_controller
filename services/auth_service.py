from fastapi import HTTPException, Depends
from sqlalchemy import select, or_, insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_session
from loggers.handler import exception_handler
from loggers.logger import (
    get_custom_logger,
    get_rotating_file_handler,
    logger_decorator,
)
from models.user_model import User
from schemas.auth_schemas import RegistrationBodySchema

from services.base.service import BaseService
from settings import settings

logger = get_custom_logger(
    logger_name=__name__,
    handlers=[get_rotating_file_handler(settings.PATH_LOG_DIR, "auth_service.log")],
)


class AuthService(BaseService):
    class Config:
        decorators = [logger_decorator(logger), exception_handler(logger)]

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def registration(self, dto: RegistrationBodySchema):
        user = (
            await self.session.execute(select(User).where(User.login == dto.login))
        ).scalar_one_or_none()
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="user with this login already exists",
            )
        user = (
            await self.session.execute(
                insert(User)
                .values(
                    **dto.dict()
                )
                .returning(User)
            )
        ).scalar_one_or_none()
        await self.session.commit()
        return user
