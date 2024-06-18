from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schemas.element_schema import ElementListResponse
from schemas.param_schema import ParamListResponse


class HistoryRegisterCreateUpdateSchema(BaseModel):
    param_id: int
    element_id: int
    value: float
    date_created: datetime


class HistoryRegisterListResponse(HistoryRegisterCreateUpdateSchema):
    id: int

    class Config:
        orm_mode = True


class HistoryInstanceResponse(HistoryRegisterListResponse):
    param: Optional[ParamListResponse]
    element: Optional[ElementListResponse]
