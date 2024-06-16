from fastapi import APIRouter, Depends, Body

from schemas.auth_schemas import RegistrationBodySchema, LoginBodySchema, RegistrationResponse, AuthorizationResponse
from services.auth_service import AuthService

router = APIRouter(prefix="/v1/auth")


@router.post(
    "/registration", summary="Регистрация", response_model=RegistrationResponse
)
async def registration(
    service: AuthService = Depends(),
    dto: RegistrationBodySchema = Body(),
):
    return await service.registration(dto=dto)


@router.post(
    "/login", summary="Авторизация", response_model=AuthorizationResponse
)
async def login(
    service: AuthService = Depends(),
    dto: LoginBodySchema = Body(),
):
    return await service.login(dto=dto)
