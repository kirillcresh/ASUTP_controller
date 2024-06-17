from datetime import datetime

from pydantic import BaseModel


class StateRegisterCreateUpdateSchema(BaseModel):
    param_id: int
    element_id: int
    value: float
    date_created: datetime


class StateRegisterListResponse(StateRegisterCreateUpdateSchema):
    id: int

    class Config:
        orm_mode = True
