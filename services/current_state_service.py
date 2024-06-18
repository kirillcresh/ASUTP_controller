from sqlalchemy import select

from loggers.handler import exception_handler
from loggers.logger import (
    get_custom_logger,
    get_rotating_file_handler,
    logger_decorator,
)
from models.current_state_model import CurrentState
from models.element_model import Element
from models.param_model import Param
from schemas.current_state_schema import CurrentStateListResponse, CurrentStateResponse
from schemas.token_schema import TokenData
from services import CommonResource
from settings import settings
from utils.paginate import PaginationRequestBodySchema, paginate

logger = get_custom_logger(
    logger_name=__name__,
    handlers=[
        get_rotating_file_handler(settings.PATH_LOG_DIR, "maintenance_service.log")
    ],
)


class CurrentStateService(CommonResource):
    class Config:
        decorators = [logger_decorator(logger), exception_handler(logger)]

    async def get_state_list(
        self, access_token_data: TokenData, pagination: PaginationRequestBodySchema
    ):
        states = await super().get_list(model=CurrentState)
        return paginate(
            data=states, dto=pagination, data_schema=CurrentStateListResponse
        )

    async def get_state_by_id(
        self, access_token_data: TokenData, current_state_id: int
    ):
        return await super().get_by_id(model=CurrentState, object_id=current_state_id)

    async def get_current_state(self, access_token_data: TokenData):
        state = await self.session.execute(
            select(
                CurrentState.id,
                CurrentState.value,
                CurrentState.update_time,
                Param.name.label("param_name"),
                Element.name.label("element_name"),
            )
            .join(Param, Param.id == CurrentState.param_id)
            .join(Element, Element.id == CurrentState.element_id)
        )
        return state.first()
