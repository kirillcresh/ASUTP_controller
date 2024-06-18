from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schemas.element_schema import ElementListResponse
from schemas.param_schema import ParamListResponse


class StateRegisterCreateUpdateSchema(BaseModel):
    param_id: int
    element_id: int
    value: float
    date_created: datetime


class StateRegisterListResponse(StateRegisterCreateUpdateSchema):
    id: int

    class Config:
        orm_mode = True


class StateInstanceResponse(StateRegisterListResponse):
    param: Optional[ParamListResponse]
    element: Optional[ElementListResponse]
