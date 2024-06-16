from fastapi import APIRouter, Depends, Body

from schemas.auth_schemas import RegistrationBodySchema, LoginBodySchema
from services.auth_service import AuthService

router = APIRouter(prefix="/v1/auth")


@router.post(
    "/registration", summary="Регистрация"
)
async def registration(
    service: AuthService = Depends(),
    dto: RegistrationBodySchema = Body(),
):
    return await service.registration(dto=dto)


@router.post(
    "/login", summary="Авторизация"
)
async def login(
    service: AuthService = Depends(),
    dto: LoginBodySchema = Body(),
):
    return await service.login(dto=dto)
