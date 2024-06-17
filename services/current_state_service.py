from models.current_state import CurrentState
from schemas.current_state_schema import CurrentStateListResponse
from schemas.token_schema import TokenData
from services import CommonResource
from utils.paginate import PaginationRequestBodySchema, paginate


class CurrentStateService(CommonResource):
    async def get_state_list(self, access_token_data: TokenData, pagination: PaginationRequestBodySchema):
        states = await super().get_list(model=CurrentState)
        return paginate(
            data=states, dto=pagination, data_schema=CurrentStateListResponse
        )

    async def get_state_by_id(self, access_token_data: TokenData, current_state_id: int):
        return await super().get_by_id(model=CurrentState, object_id=current_state_id)
