from models.current_state import CurrentState
from schemas.current_state_schema import CurrentStateListResponse
from services import CommonResource
from utils.paginate import PaginationRequestBodySchema, paginate


class CurrentStateService(CommonResource):
    async def get_state_list(self, pagination: PaginationRequestBodySchema):
        states = await super().get_list(model=CurrentState)
        return paginate(data=states, dto=pagination, data_schema=CurrentStateListResponse)

    async def get_state_by_id(self, action_id: int):
        return await super().get_by_id(model=CurrentState, id=action_id)
