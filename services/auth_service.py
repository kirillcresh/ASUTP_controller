from fastapi import Depends, HTTPException
from sqlalchemy import delete, func, insert, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from database import get_session
from loggers.handler import exception_handler
from loggers.logger import (get_custom_logger, get_rotating_file_handler,
                            logger_decorator)
from models.user_model import User
from schemas.auth_schema import (AuthorizationResponse, LoginBodySchema,
                                 RegistrationBodySchema, RegistrationResponse,
                                 UpdateUserSchema)
from schemas.token_schema import GetRefreshData, TokenData, UserPayload
from services.base.service import BaseService
from settings import settings
from utils.paginate import PaginationRequestBodySchema, paginate
from utils.security_manager import SecurityManager

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
            id=user.id, name=user.name, login=user.login, is_admin=user.is_admin
        )
        access_token, refresh_token = SecurityManager.generate_tokens(
            token_data=payload
        )
        await self._execute_upsert_user_token(
            refresh_token=refresh_token, user_id=user.id
        )
        return AuthorizationResponse(
            access_token=access_token, refresh_token=refresh_token
        )

    async def _execute_upsert_user_token(self, refresh_token: str | None, user_id: int):
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                refresh_token=(
                    SecurityManager.hash_string(refresh_token)
                    if refresh_token
                    else None
                )
            )
        )
        await self.session.commit()

    async def registration(
        self, data_dct: RegistrationBodySchema, access_token_data: TokenData
    ) -> RegistrationResponse:
        if not access_token_data.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="access forbidden",
            )
        user = (
            await self.session.execute(
                select(User).where(func.lower(User.login) == data_dct.login.lower())
            )
        ).scalar_one_or_none()
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="user with this login already exists",
            )
        data_dct.password = SecurityManager.hash_string(data_dct.password)
        user = (
            await self.session.execute(
                insert(User).values(**data_dct.dict()).returning(User)
            )
        ).scalar_one_or_none()
        await self.session.commit()
        return RegistrationResponse.from_orm(user)

    async def login(self, data_dct: LoginBodySchema) -> AuthorizationResponse:
        user = (
            await self.session.execute(
                select(User).where(func.lower(User.login) == data_dct.login.lower())
            )
        ).scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
            )
        if not SecurityManager.check_hash(data_dct.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="wrong password"
            )
        return await self._upsert_user_tokens(user=user)

    async def refresh(self, refresh_data: GetRefreshData):
        user = (
            await self.session.execute(
                select(User).where(User.id == int(refresh_data.id))
            )
        ).scalar_one_or_none()
        if not user or user.refresh_token != SecurityManager.hash_string(
            refresh_data.refresh_token
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized"
            )
        return await self._upsert_user_tokens(user=user)

    async def get_users(
        self, pagination: PaginationRequestBodySchema, access_token_data: TokenData
    ):
        """
        Получение пагинированного списка пользователей
        :param pagination: размер страницы и номер страницы
        :param access_token_data: токен пользователя
        :return: список пользователей + текущая страница и кол-во страниц
        """
        users = list((await self.session.execute(select(User))).scalars().all())
        return paginate(data=users, dto=pagination, data_schema=RegistrationResponse)

    async def get_user_current(
        self, access_token_data: TokenData
    ) -> RegistrationResponse:
        user = (
            await self.session.execute(
                select(User).where(User.id == access_token_data.id)
            )
        ).scalar_one_or_none()
        return RegistrationResponse.from_orm(user)

    async def update_user(
        self, data_dct: UpdateUserSchema, access_token_data: TokenData
    ):
        if not access_token_data.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="access forbidden",
            )
        user = (
            await self.session.execute(select(User).where(User.id == data_dct.id))
        ).scalar_one_or_none()
        user.name = data_dct.name if data_dct.name else user.name
        user.login = data_dct.login if data_dct.login else user.login
        user.password = data_dct.password if data_dct.password else user.password
        user.is_admin = data_dct.is_admin if data_dct.is_admin else user.is_admin
        await self.session.commit()
        return RegistrationResponse.from_orm(user)

    async def delete_user(self, access_token_data: TokenData, user_id: int):
        if not access_token_data.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="access forbidden",
            )
        await self.session.execute(delete(User).where(User.id == user_id))
        await self.session.commit()
        return Response(status_code=status.HTTP_201_CREATED)
