from typing import Sequence

from fastapi import APIRouter, Depends

from app.core.dependencies import (
    get_cart_service,
    get_current_user,
)
from app.models.userModel import UserModel
from app.services.cartService import CartService
from app.core.logger import logger
from app.schemas.cartSchemas import CartItemResponseSchema

router = APIRouter(
    prefix="/cart",
    tags=["cart"],
)


@router.get("/")
async def get_user_carts(
    user: UserModel = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
) -> Sequence[CartItemResponseSchema]:
    carts = await cart_service.get_user_carts(user_id=user.id)
    logger.info(f"Get carts of user with id={user.id}")
    return carts
