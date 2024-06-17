from sqlalchemy.ext.asyncio import AsyncSession

from models.action_model import Action
from schemas.action_schema import ActionListResponse
from services import CommonResource
from utils.paginate import PaginationRequestBodySchema, paginate


class ActionService(CommonResource):
    async def get_action_list(self, pagination: PaginationRequestBodySchema):
        actions = await super().get_list(model=Action)
        return paginate(data=actions, dto=pagination, data_schema=ActionListResponse)

    async def get_action_by_id(self, action_id: int):
        return await super().get_by_id(model=Action, id=action_id)
