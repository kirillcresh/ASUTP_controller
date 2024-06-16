from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from loggers.handler import exception_handler
from loggers.logger import (get_custom_logger, get_rotating_file_handler,
                            logger_decorator)
from services.base.service import BaseService
from settings import settings

logger = get_custom_logger(
    logger_name=__name__,
    handlers=[get_rotating_file_handler(settings.PATH_LOG_DIR, "auth_service.log")],
)


class CrudService(BaseService):
    class Config:
        decorators = [logger_decorator(logger), exception_handler(logger)]

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
