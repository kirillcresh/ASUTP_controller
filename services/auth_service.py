from database import get_session
from loggers.handler import exception_handler
from loggers.logger import (
    get_custom_logger,
    get_rotating_file_handler,
    logger_decorator,
)
from schemas.auth_schemas import RegistrationBodySchema

from services.base.service import BaseService
from settings import settings

logger = get_custom_logger(
    logger_name=__name__,
    handlers=[get_rotating_file_handler(settings.PATH_LOG_DIR, "auth_service.log")],
)


class AuthService(BaseService):
    class Config:
        decorators = [logger_decorator(logger), exception_handler(logger)]

    def registration(self, dto: RegistrationBodySchema):
        with get_session() as session:
            user = User(name=dto.name, login=dto.login, password=dto.password)
            session.add(user)
            session.commit()
            session.refresh(user)
        return user