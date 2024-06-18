from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schemas.element_schema import ElementListResponse
from schemas.param_schema import ParamListResponse


class CurrentStateCreateUpdateSchema(BaseModel):
    param_id: int
    element_id: int
    value: float
    update_time: datetime


class CurrentStateListResponse(CurrentStateCreateUpdateSchema):
    id: int

    class Config:
        orm_mode = True


class CurrentStateInstanceResponse(CurrentStateListResponse):
    param: Optional[ParamListResponse]
    element: Optional[ElementListResponse]


class CurrentStateResponse(BaseModel):
    id: int
    param_name: str
    element_name: str
    value: float
    update_time: datetime

    class Config:
        orm_mode = True
