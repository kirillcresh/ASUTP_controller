from math import ceil
from typing import Type

from fastapi import HTTPException
from pydantic import BaseModel, Field, parse_obj_as
from starlette import status


class PaginationRequestBodySchema(BaseModel):
    page: int = Field(ge=1, description="Текущая страница")
    page_size: int = Field(
        ge=1, le=50, description="Количество элементов для отображения на странице"
    )


class PaginationAbstractResponseSchema(BaseModel):
    total_pages: int = Field(
        description="Максимальное количество страниц с текущими параметрами page_size"
    )
    current_page: int = Field(description="Текущая страница")


def paginate(
    dto: PaginationRequestBodySchema,
    data: list = None,
    data_schema: Type[BaseModel] = None,
):
    """Производит пагинацию для страницы
    dto - тело запроса с пагинацией
    data - список элементов
    """
    total = len(data)
    total_page = ceil(total / dto.page_size)

    if data is None or dto.page > total_page:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if total > dto.page_size:
        start_item = (dto.page - 1) * dto.page_size
        final_item = dto.page * dto.page_size
        data = data[start_item:final_item]

    if data_schema:
        data = [data_schema.from_orm(item).dict() for item in data]

    response = {
        "current_page": dto.page,
        "total_pages": total_page,
        "data": data,
    }
    return response
