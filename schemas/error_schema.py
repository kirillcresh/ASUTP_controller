from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schemas.user_schema import UserListResponse


class ErrorCreateUpdateSchema(BaseModel):
    error_text: str
    closed_by: int
    date_created: datetime


class ErrorListResponse(ErrorCreateUpdateSchema):
    id: int

    class Config:
        orm_mode = True


class ErrorInstanceResponse(ErrorListResponse):
    user: Optional[UserListResponse]
