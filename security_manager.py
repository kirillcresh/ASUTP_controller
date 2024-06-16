import datetime
import hashlib
import hmac
import secrets

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status

from settings import settings

from schemas.token_schema import GetRefreshData, RefreshToken, TokenData, UserPayload


class SecurityManager:

    @staticmethod
    def hash_string(string: str) -> str:
        """Функция для хеширования кода/токена"""

        # Преобразуем секретный ключ в байтовую строку
        secret_key_bytes = settings.SECRET_KEY.encode()

        hashed_string = hmac.new(
            secret_key_bytes, string.encode(), hashlib.sha256
        ).hexdigest()
        return hashed_string

    @classmethod
    def check_hash(cls, string: str, hash_string: str) -> bool:
        """Функция для проверки хешей"""

        new_hash_string = cls.hash_string(string)
        if new_hash_string == hash_string:
            return True
        else:
            return False

    @staticmethod
    def generate_tokens(token_data: UserPayload):
        """Функция для генерации пары токенов"""
        iat = datetime.datetime.utcnow()
        access_token = jwt.encode(
            {
                **token_data.dict(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE),
                "iat": iat
            },
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        refresh_token = jwt.encode(
            {
                "id": token_data.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE),
                "iat": iat
            },
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        return access_token, refresh_token

    @classmethod
    def _decode_token(cls, token: str, raise_expired_access: bool = True):
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALGORITHM,
            options={'verify_exp': raise_expired_access},
        )

    @classmethod
    def _get_tokens_data(
            cls,
            access: str,
            refresh: str,
            raise_expired_access: bool = True
    ) -> tuple[TokenData, RefreshToken]:
        if not refresh and not access:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
        try:
            refresh_payload = cls._decode_token(refresh)
            access_payload = cls._decode_token(access, raise_expired_access=raise_expired_access)
            access_data = TokenData(**access_payload)
            refresh_data = RefreshToken(**refresh_payload)
            if access_data.iat != refresh_data.iat or access_data.id != refresh_data.id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
            return access_data, refresh_data
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")

    @classmethod
    def get_access_token_payload(
            cls,
            access: str = Depends(APIKeyHeader(name="Access", scheme_name="Access")),
            refresh: str = Depends(APIKeyHeader(name="Refresh", scheme_name="Refresh")),
    ) -> TokenData:
        """Функция для валидации токена и получения полезной нагрузки (payload).

        Используется в эндпоинтах следующим образом:
        token_data: TokenData = Depends(get_token_data)
        """
        access_payload, _ = cls._get_tokens_data(access, refresh)
        return access_payload

    @classmethod
    def get_refresh_token_data(
            cls,
            access: str = Depends(APIKeyHeader(name="Access", scheme_name="Access")),
            refresh: str = Depends(APIKeyHeader(name="Refresh", scheme_name="Refresh")),
    ) -> GetRefreshData:
        """Используется в refresh-эндпоинте"""
        _, refresh_data = cls._get_tokens_data(access, refresh, raise_expired_access=False)
        return GetRefreshData(id=refresh_data.id, refresh_token=refresh)
