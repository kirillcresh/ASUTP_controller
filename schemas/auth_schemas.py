import re

from pydantic import BaseModel, Field, validator


def validate_password(password: str):
    if len(password) < 8:
        raise ValueError("Пароль слишком короткий")
    if len(password) > 64:
        raise ValueError("Пароль слишком длинный")

    if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError("Пароль должен содержать цифру, букву и специальный символ")
    return password


class RegistrationBodySchema(BaseModel):
    name: str = Field(
        description="Имя пользователя", min_length=3, max_length=255, default="User ASUTP"
    )
    login: str = Field(
        description="Логин пользователя", min_length=3, max_length=32
    )
    password: str = Field(description="Пароль пользователя", min_length=8, max_length=64)

    @validator("password")
    def validate_strong_password(cls, password: str):
        return validate_password(password=password)
    class Config:
        orm_mode = True