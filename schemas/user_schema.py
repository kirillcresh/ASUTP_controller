from pydantic import BaseModel


class UserCreateUpdateSchema(BaseModel):
    name: str
    login: str
    password: str
    is_admin: bool
    refresh_token: str


class UserListResponse(UserCreateUpdateSchema):
    id: int

    class Config:
        orm_mode = True
