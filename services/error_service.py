from models.error_model import Error
from schemas.error_schema import ErrorListResponse
from services import CommonResource
from utils.paginate import PaginationRequestBodySchema, paginate


class ErrorService(CommonResource):
    async def get_error_list(self, pagination: PaginationRequestBodySchema):
        errors = await super().get_list(model=Error)
        return paginate(data=errors, dto=pagination, data_schema=ErrorListResponse)

    async def get_error_by_id(self, action_id: int):
        return await super().get_by_id(model=Error, id=action_id)
