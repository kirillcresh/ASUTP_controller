from models.element_model import Element
from schemas.element_schema import ElementListResponse
from services import CommonResource
from utils.paginate import PaginationRequestBodySchema, paginate


class ElementService(CommonResource):
    async def get_element_list(self, pagination: PaginationRequestBodySchema):
        elements = await super().get_list(model=Element)
        return paginate(data=elements, dto=pagination, data_schema=ElementListResponse)

    async def get_element_by_id(self, element_id: int):
        return await super().get_by_id(model=Element, object_id=element_id)
