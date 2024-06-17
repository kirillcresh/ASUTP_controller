from fastapi import APIRouter, Body, Depends, HTTPException

from schemas.auth_schema import (
    AuthorizationResponse,
    LoginBodySchema,
    RegistrationBodySchema,
    RegistrationResponse,
    UpdateUserSchema, PartialUpdateUserSchema,
)
from schemas.token_schema import GetRefreshData, TokenData
from services.auth_service import AuthService
from utils.paginate import PaginationRequestBodySchema
from utils.security_manager import SecurityManager

router = APIRouter(prefix="/v1/auth")


@router.post(
    "/registration", summary="Регистрация", response_model=RegistrationResponse
)
async def registration(
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
    service: AuthService = Depends(),
    data_dct: RegistrationBodySchema = Body(),
):
    return await service.registration(
        data_dct=data_dct, access_token_data=access_token_data
    )


@router.post("/login", summary="Авторизация", response_model=AuthorizationResponse)
async def login(
    service: AuthService = Depends(),
    data_dct: LoginBodySchema = Body(),
):
    return await service.login(data_dct=data_dct)


@router.get(
    "/refresh", summary="Обновление токенов", response_model=AuthorizationResponse
)
async def refresh(
    service: AuthService = Depends(),
    refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
):
    return await service.refresh(refresh_data)


@router.get("/get-users", summary="Получение всех пользователей")
async def get_users(
    service: AuthService = Depends(),
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
    pagination: PaginationRequestBodySchema = Depends(),
):
    return await service.get_users(pagination, access_token_data)


@router.get(
    "/get-current-user",
    summary="Получение данных текущего пользователя",
    response_model=RegistrationResponse,
)
async def get_user_current(
    service: AuthService = Depends(),
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
):
    return await service.get_user_current(access_token_data)


@router.put(
    "/update-user",
    summary="Обновление данных пользователя",
    response_model=RegistrationResponse,
)
async def update_user(
    service: AuthService = Depends(),
    data_dct: UpdateUserSchema = Body(),
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
):
    return await service.update_user(data_dct, access_token_data)


@router.delete("/delete-user", summary="Удаление пользователя")
async def delete_user(
    user_id: int,
    service: AuthService = Depends(),
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
):
    return await service.delete_user(access_token_data, user_id)


@router.patch("/{user_id}", summary="Обновление записи пользователя")
async def partial_update_user(
    user_id: int,
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
    service: AuthService = Depends(),
    data_dct: PartialUpdateUserSchema = Body(),
):
    user = await service.get_user_by_id(
        access_token_data=access_token_data,
        user_id=user_id
    )
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User с ID {user_id} не найден"
        )
    await service.partial_update_user(
        access_token_data=access_token_data,
        user_id=user_id,
        fields=data_dct.dict()
    )
    user = await service.get_user_by_id(
        access_token_data=access_token_data,
        user_id=user_id)
    return user
