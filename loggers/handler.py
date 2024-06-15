import asyncio
import logging
from functools import wraps
from fastapi import HTTPException


def exception_handler(logger=logging.getLogger()):
    """Декоратор для ловли и обработки ошибок сервисов (service)."""

    def func_decorator(func):
        if asyncio.iscoroutinefunction(func):
            # асинхронная версия функции-обёртки
            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    result = await func(*args, **kwargs)
                except HTTPException as e:
                    raise e
                except Exception as e:
                    logger.error(e, exc_info=True)
                    if len(str(e)) > 160:
                        logger.error(f"Full error: {str(e)}")
                    raise HTTPException(e)  # noqa
                else:
                    return result

        else:
            # синхронная версия функции-обёртки
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    result = func(*args, **kwargs)
                except HTTPException as e:
                    raise e
                except Exception as e:
                    logger.error(e, exc_info=True)
                    if len(str(e)) > 160:
                        logger.error(f"Full error: {str(e)}")
                    raise HTTPException(e)  # noqa
                else:
                    return result

        return wrapper

    return func_decorator
