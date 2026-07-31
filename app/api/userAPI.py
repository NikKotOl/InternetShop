from fastapi import APIRouter, Depends

from app.core.dependencies import get_user_service
from app.schemas.tokenSchemas import TokenResponseSchema
from app.schemas.userSchemas import (
    UserCreateSchema,
    UserLoginSchema,
    UserResponseSchema,
)
from app.services.userService import UserService
from app.core.security import create_access_token
from app.core.logger import logger

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponseSchema)
async def register(
    data: UserCreateSchema, user_service: UserService = Depends(get_user_service)
):
    user = await user_service.register_user(
        username=data.username, password=data.password
    )
    logger.info(f"User with username '{user.username}' was registered")
    return UserResponseSchema.model_validate(user)


@router.post("/login", response_model=TokenResponseSchema)
async def login(
    data: UserLoginSchema, user_service: UserService = Depends(get_user_service)
):
    user = await user_service.authenticate_user(
        username=data.username, password=data.password
    )
    logger.info(f"User {data.username} logged in successfully")

    token = create_access_token(user.id)
    return TokenResponseSchema(access_token=token, token_type="bearer")
