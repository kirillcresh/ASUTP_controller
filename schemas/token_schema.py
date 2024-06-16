from datetime import datetime

from pydantic import BaseModel


class UserPayload(BaseModel):
    id: int
    name: str
    login: str
    is_admin: bool


class RefreshToken(BaseModel):
    id: int
    iat: datetime
    exp: datetime


class TokenData(UserPayload, RefreshToken):
    pass


class GetRefreshData(BaseModel):
    id: str
    refresh_token: str
