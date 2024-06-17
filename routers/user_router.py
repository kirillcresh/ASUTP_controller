from fastapi import APIRouter, Depends, HTTPException

from schemas.user_schema import UserListResponse
from schemas.token_schema import GetRefreshData
from services.user_service import UserService
from utils.paginate import PaginationRequestBodySchema
from utils.security_manager import SecurityManager

router = APIRouter(prefix="/v1/user")


@router.get("/list", summary="Список User")
async def get_user_list_router(
    service: UserService = Depends(),
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
    pagination: PaginationRequestBodySchema = Depends(),
):
    users = await service.get_user_list(
        # refresh_data=refresh_data,
        pagination=pagination
    )
    return users


@router.get(
    "/{user_id}",
    summary="Получить User по ID",
    response_model=UserListResponse,
)
async def get_user_by_id_router(
    user_id: int,
    service: UserService = Depends()
    # refresh_data: GetRefreshData = Depends(SecurityManager.get_refresh_token_data),
):
    user = await service.get_user_by_id(
        # refresh_data=refresh_data,
        user_id=user_id
    )
    if not user:
        raise HTTPException(
            status_code=404, detail=f"Param с ID {user_id} не найден"
        )
    return user
