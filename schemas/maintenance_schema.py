from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator

from schemas.action_schema import ActionListResponse
from schemas.user_schema import UserListResponse


def validate_value(value: float | None):
    decimal_places = 3
    if value and round(value, decimal_places) != value:
        raise ValueError(f'Значение должно содержать 3 цифры после запятой')

    return value


class MaintenanceBodySchema(BaseModel):
    action_id: int = Field(
        description="ID действия (обязательное поле)",
    )
    created_by: int = Field(
        description="ID пользователя (обязательное поле)",
    )
    description: str = Field(description="Описание действия")
    value: float | None = Field(description="Значение показателя, если валидно")
    date_created: datetime = Field(
        description="Дата создания записи", default=datetime.utcnow()
    )

    @validator("value")
    def validate_value(cls, value: float):
        return validate_value(value)


class PartialMaintenanceBodySchema(BaseModel):
    action_id: Optional[int] = None
    created_by: Optional[int] = None
    description: Optional[str] = None
    value: Optional[float] = None
    date_created: Optional[datetime] = None

    @validator("value")
    def validate_value(cls, value: float):
        return validate_value(value)


class MaintenanceResponse(MaintenanceBodySchema):
    id: int

    class Config:
        orm_mode = True


class MaintenanceInstanceResponse(MaintenanceResponse):
    action: Optional[ActionListResponse]
    user: Optional[UserListResponse]
