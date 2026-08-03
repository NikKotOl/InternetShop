from typing import Sequence

from fastapi import APIRouter, Depends

from app.core.dependencies import (
    get_cart_service,
    get_current_user,
)
from app.models.userModel import UserModel
from app.services.cartService import CartService
from app.core.logger import logger
from app.schemas.cartSchemas import (
    CartAddResponseSchema,
    CartAddSchema,
    CartItemResponseSchema,
    UpdateQuantitySchema,
)

router = APIRouter(
    prefix="/cart",
    tags=["cart"],
)


@router.get("/")
async def get_user_carts_items(
    user: UserModel = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
) -> Sequence[CartItemResponseSchema]:
    carts = await cart_service.get_user_cart_items(user_id=user.id)
    logger.info(f"Get carts of user with id={user.id}")
    return carts


@router.post("/")
async def add_cart(
    cart: CartAddSchema,
    user: UserModel = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
) -> CartAddResponseSchema:
    response = await cart_service.add_to_cart(user.id, cart.product_id, cart.quantity)
    logger.info(
        f"Added cart with user_id={user.id}, product_id={cart.product_id}, quantity={cart.quantity}"
    )
    return CartAddResponseSchema.model_validate(response)


@router.patch("/{cart_id}")
async def update_quantity(
    cart_id: int,
    data: UpdateQuantitySchema,
    user: UserModel = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
) -> CartAddResponseSchema:
    response = await cart_service.update_quantity(user.id, cart_id, data.quantity)
    logger.info(f"Update quantity in cart with id={cart_id}")
    return CartAddResponseSchema.model_validate(response)


@router.delete("/{cart_id}")
async def delete_cart_item(
    cart_id: int,
    user: UserModel = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
) -> CartAddResponseSchema:
    response = await cart_service.delete_cart_item(user.id, cart_id)
    logger.info(f"Deleted cart item with cart id={cart_id}")
    return CartAddResponseSchema.model_validate(response)
