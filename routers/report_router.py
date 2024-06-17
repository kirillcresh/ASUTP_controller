from fastapi import APIRouter, Depends, HTTPException

from schemas.report_schema import ReportListResponse
from schemas.token_schema import GetRefreshData
from services.report_service import ReportService
from utils.paginate import PaginationRequestBodySchema
from utils.security_manager import SecurityManager

router = APIRouter(prefix="/v1/report")


@router.get("/list", summary="Список Report")
async def get_report_list_router(
    service: ReportService = Depends(),
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
    pagination: PaginationRequestBodySchema = Depends(),
):
    reports = await service.get_report_list(
        # refresh_data=refresh_data,
        pagination=pagination
    )
    return reports


@router.get(
    "/{report_id}",
    summary="Получить Report по ID",
    response_model=ReportListResponse,
)
async def get_report_by_id_router(
    report_id: int,
    service: ReportService = Depends()
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
):
    report = await service.get_report_by_id(
        # refresh_data=refresh_data,
        report_id=report_id
    )
    if not report:
        raise HTTPException(
            status_code=404, detail=f"Report с ID {report_id} не найден"
        )
    return report
