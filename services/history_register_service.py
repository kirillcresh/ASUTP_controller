import csv
import io
import re
from datetime import date, datetime

from fastapi import HTTPException, Response
from starlette.responses import FileResponse, StreamingResponse

from models.history_register_model import HistoryRegister
from schemas.history_register_schema import (
    CSVHistoryResponse,
    HistoryInstanceResponse,
    HistoryRegisterListResponse,
)
from schemas.token_schema import TokenData
from services import CommonResource
from utils.paginate import PaginationRequestBodySchema, paginate


class HistoryRegisterService(CommonResource):
    async def get_history_register_list(
        self, access_token_data: TokenData, pagination: PaginationRequestBodySchema
    ):
        history_registers = await super().get_list(model=HistoryRegister)
        return paginate(
            data=history_registers,
            dto=pagination,
            data_schema=HistoryRegisterListResponse,
        )

    async def get_history_register_by_id(
        self, access_token_data: TokenData, history_register_id: int
    ):
        return await super().get_by_id(
            model=HistoryRegister, object_id=history_register_id
        )

    async def get_history_csv(
        self, date_from: str | date, date_to: str | date, access_token_data: TokenData
    ):
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(pattern, date_from) or not re.match(pattern, date_to):
            raise HTTPException(
                status_code=400, detail="Неправильный формат даты (ГГГГ-ММ-ДД)"
            )
        try:
            date_from_stmp = datetime.strptime(date_from, "%Y-%m-%d")
            date_to_stmp = datetime.strptime(date_to, "%Y-%m-%d")
            history_registers = await super().get_list(
                model=HistoryRegister,
                conditions=[
                    (HistoryRegister.date_created >= date_from_stmp),
                    (HistoryRegister.date_created <= date_to_stmp),
                ],
            )
            if history_registers:
                fieldnames = ["id", "param", "element", "value", "date_created"]
                buffer = io.StringIO()
                writer = csv.DictWriter(buffer, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(
                    CSVHistoryResponse.from_orm(history).dict()
                    for history in history_registers
                )
                buffer.seek(0)
                response = StreamingResponse(
                    iter(buffer.getvalue()), media_type="text/csv"
                )
                response.headers[
                    "Content-Disposition"
                ] = f"attachment; filename=history_register{date_from}to{date_to}.csv"
                return response
            else:
                raise HTTPException(status_code=404, detail="Нет данных")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
