from datetime import datetime

from pydantic import BaseModel


class ElementCreateUpdateSchema(BaseModel):
    name: str


class ElementListResponse(ElementCreateUpdateSchema):
    id: int

    class Config:
        orm_mode = True
