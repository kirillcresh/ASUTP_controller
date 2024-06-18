from models.param_model import Param
from schemas.param_schema import ParamListResponse
from schemas.token_schema import TokenData
from services import CommonResource
from utils.paginate import PaginationRequestBodySchema, paginate


class ParamService(CommonResource):
    async def get_param_list(
        self, access_token_data: TokenData, pagination: PaginationRequestBodySchema
    ):
        params = await super().get_list(model=Param)
        return paginate(data=params, dto=pagination, data_schema=ParamListResponse)

    async def get_param_by_id(self, access_token_data: TokenData, param_id: int):
        return await super().get_by_id(model=Param, object_id=param_id)
