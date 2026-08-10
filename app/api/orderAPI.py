from fastapi import APIRouter, Depends

from app.core.dependencies import (
    get_current_user,
    get_order_repository,
    get_order_service,
)
from app.models.userModel import UserModel
from app.repositories.orderRepository import OrderRepository
from app.schemas.orderSchemas import OrderResponseSchema, OrderItemResponseSchema
from app.services.orderService import OrderService
from app.core.logger import logger

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.get("/")
async def get_orders(
    order_repository: OrderRepository = Depends(get_order_repository),
    user: UserModel = Depends(get_current_user),
) -> list[OrderResponseSchema]:
    orders = await order_repository.get_orders_by_user_id(user.id)
    logger.info(f"Get orders from a user with id={user.id}")
    return [
        OrderResponseSchema(
            id=order.id,
            created_at=order.created_at,
            items=[OrderItemResponseSchema.model_validate(i) for i in items],
        )
        for order, items in orders
    ]


@router.get("/{order_id}")
async def get_order_by_id(
    order_id: int,
    user: UserModel = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
) -> OrderResponseSchema:
    response = await order_service.get_order_by_id(order_id, user.id)
    logger.info(f"Get order with id={order_id}")
    return OrderResponseSchema(
        id=response[0].id,
        created_at=response[0].created_at,
        items=[OrderItemResponseSchema.model_validate(i) for i in response[1]],
    )


@router.post("/", status_code=201)
async def create_order(
    user: UserModel = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
) -> OrderResponseSchema:
    order, items = await order_service.create_order(user.id)
    logger.info(f"Created order with id={order.id}")
    return OrderResponseSchema(
        id=order.id,
        created_at=order.created_at,
        items=[OrderItemResponseSchema.model_validate(i) for i in items],
    )
