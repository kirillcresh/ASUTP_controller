from typing import Any, Dict

from fastapi import Depends
from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_session


class CommonResource:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_list(self, model, conditions=None):
        query = select(model)
        if conditions:
            query = query.filter(*conditions)
        query_join = inspect(model)
        for rel in list(query_join.relationships):
            query = query.options(selectinload(getattr(model, rel.key)))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, model, object_id):
        query = select(model).where(model.id == object_id)
        query_join = inspect(model)
        for rel in list(query_join.relationships):
            query = query.options(selectinload(getattr(model, rel.key)))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, model, **kwargs):
        instance = model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, model, object_id: int, **kwargs):
        query = select(model).where(model.id == object_id)
        result = await self.session.execute(query)
        instance = result.scalar_one_or_none()
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def partial_update(self, model, object_id: int, fields: Dict[str, Any]):
        query = select(model).where(model.id == object_id)
        result = await self.session.execute(query)
        instance = result.scalar_one_or_none()

        for key, value in fields.items():
            if value is not None and hasattr(instance, key):
                setattr(instance, key, value)

        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, model, object_id: int):
        query = select(model).where(model.id == object_id)
        result = await self.session.execute(query)
        instance = result.scalar_one_or_none()
        await self.session.delete(instance)
        await self.session.commit()
        return instance
