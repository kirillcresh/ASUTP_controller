import asyncio
import logging
import time
import warnings
from collections.abc import Sequence
from functools import wraps
from logging.handlers import RotatingFileHandler
from pathlib import Path

MEGABYTE = 1024 * 1024
FORMATTER = logging.Formatter(
    "{asctime} [{levelname}] {name}:{filename}:{funcName}.{lineno} - {message}",
    style="{",
)


def init_logging(
    PATH_DIR: Path = Path("logs"),
    level_base: str = "DEBUG",
    level_file: str = "DEBUG",
    level_console: str = "INFO",
    formatter=FORMATTER,
):
    """Инициализация логирования"""

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level=level_console)
    console_handler.setFormatter(formatter)

    file_handler = get_rotating_file_handler(
        PATH_DIR, "root.log", level_file, formatter
    )

    logging.basicConfig(
        level=level_base,
        format=formatter._fmt,
        style="{",
        handlers=[console_handler, file_handler],
    )


def get_rotating_file_handler(
    PATH_DIR: Path, filename: str, level: str = "DEBUG", formatter=FORMATTER
):
    """Возвращает стандартизированный файловый обработчик."""
    handler = RotatingFileHandler(
        f"{PATH_DIR}/{filename}",
        mode="a",
        maxBytes=MEGABYTE * 5,
        backupCount=5,
        encoding="utf-8",
    )
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler


def get_custom_logger(
    logger_name: str = None, handlers: Sequence = (), formatter=FORMATTER
):
    """Возвращает логгер с добавленными обработчиками handlers и форматированием formatter."""
    warnings.warn("Рекомендуется использовать get_logger", DeprecationWarning)

    logger = logging.getLogger(logger_name) if logger_name else logging.getLogger()
    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def get_logger(name, level: str = "DEBUG", path_dir: Path = Path("logs")):
    """Возвращает логгер по его имени с файловым обработчиком и устанавливает
    ему уровень логирования."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(
        get_rotating_file_handler(
            PATH_DIR=path_dir,
            filename=f"{name}.log",
            level=level,
        )
    )
    return logger


def logger_decorator(logger=logging.getLogger()):
    """Декоратор для логгирования функций."""

    def func_decorator(func):
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def wrapper(*args, **kwargs):
                logger.info(
                    f"async function {func.__name__}() is running with args: {args} {kwargs}"
                )
                start = time.time()
                result = await func(*args, **kwargs)
                logger.info(
                    f"async function {func.__name__}() has finished in {time.time() - start:.4f} seconds"
                )
                return result

        else:

            @wraps(func)
            def wrapper(*args, **kwargs):
                logger.info(
                    f"function {func.__name__}() is running with args: {args} {kwargs}"
                )
                start = time.time()
                result = func(*args, **kwargs)
                logger.info(
                    f"function {func.__name__}() has finished in {time.time() - start:.4f} seconds"
                )
                return result

        return wrapper

    return func_decorator
