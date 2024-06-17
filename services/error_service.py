from models.error_model import Error
from schemas.error_schema import ErrorListResponse
from schemas.token_schema import TokenData
from services import CommonResource
from utils.paginate import PaginationRequestBodySchema, paginate


class ErrorService(CommonResource):
    async def get_error_list(self, access_token_data: TokenData, pagination: PaginationRequestBodySchema):
        errors = await super().get_list(model=Error)
        return paginate(data=errors, dto=pagination, data_schema=ErrorListResponse)

    async def get_error_by_id(self, access_token_data: TokenData, error_id: int):
        return await super().get_by_id(model=Error, object_id=error_id)
