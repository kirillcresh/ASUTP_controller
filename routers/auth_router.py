from fastapi import APIRouter, Depends, Body

from schemas.auth_schemas import RegistrationBodySchema, LoginBodySchema, RegistrationResponse, AuthorizationResponse
from schemas.token_schema import TokenData, GetRefreshData
from security_manager import SecurityManager
from services.auth_service import AuthService

router = APIRouter(prefix="/v1/auth")


@router.post(
    "/registration", summary="Регистрация", response_model=RegistrationResponse
)
async def registration(
    access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
    service: AuthService = Depends(),
    dto: RegistrationBodySchema = Body(),
):
    return await service.registration(dto=dto, access_token_data=access_token_data)


@router.post(
    "/login", summary="Авторизация", response_model=AuthorizationResponse
)
async def login(
    service: AuthService = Depends(),
    dto: LoginBodySchema = Body(),
):
    return await service.login(dto=dto)


@router.get(
    "/refresh", summary="Обновление токенов", response_model=AuthorizationResponse
)
async def refresh(
    service: AuthService = Depends(),
    refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
):
    return await service.refresh(refresh_data)
