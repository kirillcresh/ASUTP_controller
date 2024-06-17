from models.history_register_model import HistoryRegister
from schemas.history_register_schema import HistoryRegisterListResponse
from services import CommonResource
from utils.paginate import PaginationRequestBodySchema, paginate


class HistoryRegisterService(CommonResource):
    async def get_history_register_list(self, pagination: PaginationRequestBodySchema):
        history_registers = await super().get_list(model=HistoryRegister)
        return paginate(
            data=history_registers,
            dto=pagination,
            data_schema=HistoryRegisterListResponse,
        )

    async def get_history_register_by_id(self, history_register_id: int):
        return await super().get_by_id(
            model=HistoryRegister, object_id=history_register_id
        )
