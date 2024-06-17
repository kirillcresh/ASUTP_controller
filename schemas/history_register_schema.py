from datetime import datetime

from pydantic import BaseModel


class HistoryRegisterCreateUpdateSchema(BaseModel):
    param_id: int
    element_id: int
    value: float
    date_created: datetime


class HistoryRegisterListResponse(HistoryRegisterCreateUpdateSchema):
    id: int

    class Config:
        orm_mode = True
