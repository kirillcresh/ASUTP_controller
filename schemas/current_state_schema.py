from datetime import datetime

from pydantic import BaseModel


class CurrentStateCreateUpdateSchema(BaseModel):
    param_id: int
    element_id: int
    value: float
    update_time: datetime


class CurrentStateListResponse(CurrentStateCreateUpdateSchema):
    id: int

    class Config:
        orm_mode = True
