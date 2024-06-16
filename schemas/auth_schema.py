import re

from pydantic import BaseModel, Field, validator


def validate_password(password: str):
    if len(password) < 8:
        raise ValueError("Пароль слишком короткий")
    if len(password) > 64:
        raise ValueError("Пароль слишком длинный")

    if (
        not re.search(r"[A-Za-z]", password)
        or not re.search(r"\d", password)
        or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    ):
        raise ValueError("Пароль должен содержать цифру, букву и специальный символ")
    return password


class RegistrationBodySchema(BaseModel):
    name: str = Field(
        description="Имя пользователя",
        min_length=3,
        max_length=255,
        default="User ASUTP",
    )
    login: str = Field(description="Логин пользователя", min_length=3, max_length=32)
    password: str = Field(
        description="Пароль пользователя", min_length=8, max_length=64
    )
    is_admin: bool = Field(description="Администратор", default=False)

    @validator("password")
    def validate_strong_password(cls, password: str):
        return validate_password(password=password)


class RegistrationResponse(BaseModel):
    id: int
    name: str
    login: str
    is_admin: bool

    class Config:
        orm_mode = True


class LoginBodySchema(BaseModel):
    login: str = Field(description="Логин пользователя", min_length=3, max_length=32)
    password: str = Field(
        description="Пароль пользователя", min_length=8, max_length=64
    )


class AuthorizationResponse(BaseModel):
    access_token: str
    refresh_token: str


class UpdateUserSchema(BaseModel):
    id: int = Field(description="ID пользователя")
    name: str | None = Field(
        description="Имя пользователя",
        min_length=3,
        max_length=255,
        default="User ASUTP",
    )
    login: str | None = Field(
        description="Логин пользователя", min_length=3, max_length=32
    )
    password: str | None = Field(
        description="Пароль пользователя", min_length=8, max_length=64
    )
    is_admin: bool | None = Field(description="Администратор", default=False)

    @validator("password")
    def validate_strong_password(cls, password: str):
        return validate_password(password=password)
