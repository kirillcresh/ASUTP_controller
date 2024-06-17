from datetime import datetime

from pydantic import BaseModel


class ReportCreateUpdateSchema(BaseModel):
    created_by: int
    filename: str
    date_created: datetime


class ReportListResponse(ReportCreateUpdateSchema):
    id: int

    class Config:
        orm_mode = True
