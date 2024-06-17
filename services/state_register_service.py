from models.state_register_model import StateRegister
from schemas.state_register_schema import StateRegisterListResponse
from schemas.token_schema import TokenData
from services import CommonResource
from utils.paginate import PaginationRequestBodySchema, paginate


class StateRegisterService(CommonResource):
    async def get_state_register_list(self, access_token_data: TokenData, pagination: PaginationRequestBodySchema):
        states = await super().get_list(model=StateRegister)
        return paginate(
            data=states, dto=pagination, data_schema=StateRegisterListResponse
        )

    async def get_state_register_by_id(self, access_token_data: TokenData, state_register_id: int):
        return await super().get_by_id(model=StateRegister, object_id=state_register_id)
