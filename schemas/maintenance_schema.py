from datetime import datetime

from pydantic import BaseModel, Field


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


class MaintenanceResponse(MaintenanceBodySchema):
    id: int

    class Config:
        orm_mode = True
