from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schemas.user_schema import UserListResponse


class ReportCreateUpdateSchema(BaseModel):
    created_by: int
    filename: str
    date_created: datetime


class ReportListResponse(ReportCreateUpdateSchema):
    id: int

    class Config:
        orm_mode = True


class ReportInstanceResponse(ReportListResponse):
    user: Optional[UserListResponse]
