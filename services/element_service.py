from models.element_model import Element
from schemas.element_schema import ElementListResponse
from schemas.token_schema import TokenData
from services import CommonResource
from utils.paginate import PaginationRequestBodySchema, paginate


class ElementService(CommonResource):
    async def get_element_list(self, access_token_data: TokenData, pagination: PaginationRequestBodySchema):
        elements = await super().get_list(model=Element)
        return paginate(data=elements, dto=pagination, data_schema=ElementListResponse)

    async def get_element_by_id(self, access_token_data: TokenData, element_id: int):
        return await super().get_by_id(model=Element, object_id=element_id)
