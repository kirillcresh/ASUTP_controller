from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from schemas.action_schema import ActionListResponse
from schemas.maintenance_schema import MaintenanceResponse
from utils.paginate import PaginationRequestBodySchema, paginate


class CommonResource:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_list(self, model, pagination: PaginationRequestBodySchema, conditions=None):
        query = select(model)
        if conditions:
            query = query.filter(*conditions)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, model, id):
        query = select(model).where(model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
