from pydantic import BaseModel


class ParamCreateUpdateSchema(BaseModel):
    dimension: str
    name: str
    type: int


class ParamListResponse(ParamCreateUpdateSchema):
    id: int

    class Config:
        orm_mode = True
