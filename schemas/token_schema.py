from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.class_validators import root_validator, validator
from pydantic.networks import EmailStr



class UserPayload(BaseModel):
    id: int
    first_name: str
    phone: str | None
    email: str | None
    last_name: str | None
    verify_phone: bool
    verify_email: bool


class RefreshToken(BaseModel):
    id: int
    iat: datetime
    exp: datetime


class TokenData(UserPayload, RefreshToken):
    pass


class GetRefreshData(BaseModel):
    id: str
    refresh_token: str
