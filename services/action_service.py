from models.action_model import Action
from schemas.action_schema import ActionListResponse
from schemas.token_schema import TokenData
from services import CommonResource
from utils.paginate import PaginationRequestBodySchema, paginate


class ActionService(CommonResource):
    async def get_action_list(
        self, access_token_data: TokenData, pagination: PaginationRequestBodySchema
    ):
        actions = await super().get_list(model=Action)
        return paginate(data=actions, dto=pagination, data_schema=ActionListResponse)

    async def get_action_by_id(self, access_token_data: TokenData, action_id: int):
        return await super().get_by_id(model=Action, object_id=action_id)
