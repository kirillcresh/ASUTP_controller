from datetime import datetime

from pydantic import BaseModel


class ErrorCreateUpdateSchema(BaseModel):
    error_text: str
    closed_by: int
    date_created: datetime


class ErrorListResponse(ErrorCreateUpdateSchema):
    id: int

    class Config:
        orm_mode = True
