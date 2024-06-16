from fastapi import APIRouter, Depends

from schemas.token_schema import TokenData
from utils.security_manager import SecurityManager
from services.crud_service import CrudService

router = APIRouter(prefix="/v1/crud")

# @router.post(
#     "/", summary="Регистрация"
# )
# async def registration(
#     access_token_data: TokenData = Depends(SecurityManager.get_access_token_payload),
#     service: CrudService = Depends(),
#     dto: RegistrationBodySchema = Body(),
# ):
#     return await service.registration(dto=dto, access_token_data=access_token_data)