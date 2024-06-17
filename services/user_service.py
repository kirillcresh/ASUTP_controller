from models.user_model import User
from schemas.user_schema import UserListResponse
from services import CommonResource
from utils.paginate import PaginationRequestBodySchema, paginate


class UserService(CommonResource):
    async def get_user_list(self, pagination: PaginationRequestBodySchema):
        users = await super().get_list(model=User)
        return paginate(data=users, dto=pagination, data_schema=UserListResponse)

    async def get_user_by_id(self, user_id: int):
        return await super().get_by_id(model=User, object_id=user_id)
