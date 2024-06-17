from pydantic import BaseModel


class ActionCreateUpdateSchema(BaseModel):
    name: str


class ActionListResponse(ActionCreateUpdateSchema):
    id: int

    class Config:
        orm_mode = True
