from models.report_model import Report
from schemas.report_schema import ReportListResponse
from schemas.token_schema import TokenData
from services import CommonResource
from utils.paginate import PaginationRequestBodySchema, paginate


class ReportService(CommonResource):
    async def get_report_list(self, access_token_data: TokenData, pagination: PaginationRequestBodySchema):
        reports = await super().get_list(model=Report)
        return paginate(data=reports, dto=pagination, data_schema=ReportListResponse)

    async def get_report_by_id(self, access_token_data: TokenData, report_id: int):
        return await super().get_by_id(model=Report, object_id=report_id)
