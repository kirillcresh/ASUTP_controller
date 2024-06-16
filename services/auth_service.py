from fastapi import HTTPException, Depends
from sqlalchemy import select, or_, insert, func
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
from schemas.auth_schemas import RegistrationBodySchema, LoginBodySchema, AuthorizationResponse, RegistrationResponse
from schemas.token_schema import UserPayload
from security_manager import SecurityManager

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

    async def _upsert_user_tokens(self, user: User):
        payload = UserPayload(
            id=user.id,
            name=user.name,
            login=user.login
        )
        access_token, refresh_token = SecurityManager.generate_tokens(
            token_data=payload
        )
        return AuthorizationResponse(
            access_token=access_token, refresh_token=refresh_token
        )

    async def registration(self, dto: RegistrationBodySchema) -> RegistrationResponse:
        user = (
            await self.session.execute(select(User).where(func.lower(User.login) == dto.login.lower()))
        ).scalar_one_or_none()
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="user with this login already exists",
            )
        dto.password = SecurityManager.hash_string(dto.password)
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
        return RegistrationResponse.from_orm(user)

    async def login(self, dto: LoginBodySchema) -> AuthorizationResponse:
        user = (
            await self.session.execute(
                select(User).where(func.lower(User.login) == dto.login.lower())
            )
        ).scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        if not SecurityManager.check_hash(dto.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="wrong password")
        return await self._upsert_user_tokens(user=user)
