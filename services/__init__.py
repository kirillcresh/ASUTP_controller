from enum import Enum
from typing import Union

from fastapi import HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import UUID4
from sqlalchemy import asc, delete, desc, select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from database import get_session


class SortOrder(str, Enum):
    DESC = "DESC"
    ASC = "ASC"


class CommonResource:
    model = None
    create_update_schema = None
    auth = None
    lookup_field = "id"

    @staticmethod
    def get_filter_expressions(model, kwargs: dict):
        filter_expressions = []
        for kw_name, kw_value in kwargs.items():
            filter_expressions.append(getattr(model, kw_name) == kw_value)
        return filter_expressions

    @staticmethod
    def get_ordering(sort_field: str, sort_order: str):
        return (
            asc(sort_field) if sort_order == SortOrder.ASC.value else desc(sort_field)
        )

    async def get_select(
        self,
        model,
        where_kwargs,
        sort_field=lookup_field,
        sort_order=SortOrder.ASC.value,
    ):
        return (
            select(model)
            .where(*self.get_filter_expressions(model, where_kwargs))
            .order_by(self.get_ordering(sort_field, sort_order))
        )

    async def get_or_404(self, by, model):
        session = await get_session()
        where_kwargs = {self.lookup_field: by}
        query = await self.get_select(model, where_kwargs)
        existing_instance = (await session.scalars(query)).first()
        if not existing_instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return session, existing_instance

    async def get_list(
        self,
        model,
        sort_field: str = lookup_field,
        sort_order: str = SortOrder.ASC.value,
        skip: int = 0,
        limit: int = 100,
        **kwargs,
    ):
        session = await get_session()
        query = await self.get_select(model, kwargs, sort_field, sort_order)
        result = await session.execute(query)
        await session.close()
        return [dict(row) for row in result.scalars().all()][skip: skip + limit]  # fmt: skip

    async def create(self, new, model, token_data):
        new_object = model(**new.dict(exclude_none=True))
        session = await get_session()
        session.add(new_object)
        try:
            await session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{model.__name__} с данным именем уже существует",
            )
        await session.refresh(new_object)
        return JSONResponse(
            jsonable_encoder(new_object), status_code=status.HTTP_201_CREATED
        )

    async def get_instance(self, by: Union[int, UUID4], model):
        _, instance = await self.get_or_404(by, model)
        return instance

    async def update_instance(
        self, by: Union[int, UUID4], editable: create_update_schema, model
    ):
        session, instance = await self.get_or_404(by, model)
        await session.execute(
            update(model)
            .where(getattr(model, self.lookup_field) == by)
            .values(**editable.dict())
        )
        await session.commit()
        return instance

    async def delete_instance(self, by: Union[int, UUID4], model):
        session, _ = await self.get_or_404(by, model)
        await session.execute(
            delete(model).where(getattr(model, self.lookup_field) == by)
        )
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @staticmethod
    async def flush_session(session):
        try:
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"{e.__dict__['orig'].__cause__.message}. {e.__dict__['orig'].__cause__.detail or ''}",
            )
