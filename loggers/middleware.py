import json
import logging
import typing
from typing import Callable

from fastapi import FastAPI, Request, Response
from starlette.background import BackgroundTask
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message


class LoggerMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        *,
        logger: typing.Optional[logging.Logger] = None,
        log_body_always: bool = False,
    ):
        """
        Прослойка для логирования запроса.
        Логирует запрос. По умолчанию пишется в лог: метод, статус код, url, ip клиента.
        Если запрос завершился ошибкой, то добавляет поля: тела запроса и ответа.
        Тело запроса или ответа логируется, только если они являются json.
        :param logger - логер, куда будет писаться лог
        :param log_body_always - логировать тело запроса и ответа даже, когда не произошла ошибка
        """
        self._logger = logger if logger else logging.getLogger()
        self.log_body_always = log_body_always
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if "application/json" in request.headers.get("Content-Type", ""):
            # https://stackoverflow.com/questions/69669808/fastapi-custom-middleware-getting-body-of-request-inside
            await self.set_body(request)

        response: Response = await call_next(request)

        error = response.status_code >= 400
        log_str = await self.generate_log_str(request, response, error)

        # https://stackoverflow.com/questions/72372029/fastapi-background-task-in-middleware
        response.background = BackgroundTask(self.log_request, log_str, error)
        return response

    async def generate_log_str(
        self, request: Request, response: Response, error: bool
    ) -> str:
        url = request.url.path
        if request.query_params:
            url += "?" + str(request.query_params)
        log_str = f"{request.method} {response.status_code} {url}, client={request.client.host}"

        if self.log_body_always or error:
            if "application/json" in request.headers.get("Content-Type", ""):
                try:
                    body = await request.json()
                    log_str += f", request_body={body}"
                except Exception:
                    log_str += f", request_body_error = JSONDecodeError"
            if "application/json" in response.headers.get("Content-Type", ""):
                # https://stackoverflow.com/questions/71882419/fastapi-how-to-get-the-response-body-in-middleware
                response_body = [chunk async for chunk in response.body_iterator]
                response.body_iterator = iterate_in_threadpool(iter(response_body))
                log_str += f", response_body={json.loads(response_body[0].decode())}"
        return log_str

    def log_request(self, log_str: str, error: bool) -> None:
        if error:
            self._logger.error(log_str)
        else:
            self._logger.info(log_str)

    async def set_body(self, request: Request) -> None:
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive
