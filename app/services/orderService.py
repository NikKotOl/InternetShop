from app.core.exceptions import EmptyCartError, OrderNotFoundError
from app.models.orderModel import OrderItemModel, OrderModel
from app.repositories.cartRepository import CartRepository
from app.repositories.orderRepository import OrderRepository


class OrderService:
    order_repository: OrderRepository
    cart_repository: CartRepository

    def __init__(
        self,
        order_repository: OrderRepository,
        cart_repository: CartRepository,
    ):
        self.order_repository = order_repository
        self.cart_repository = cart_repository

    async def create_order(self, user_id: int) -> OrderModel:
        cart_items = await self.cart_repository.get_cart_items_with_products_by_user_id(
            user_id
        )
        if not cart_items:
            raise EmptyCartError(user_id)
        order = await self.order_repository.add_order(user_id)
        for item in cart_items:
            await self.order_repository.add_order_item(
                order_id=order.id,
                product_id=item[0].product_id,
                product_name=item[1].name,
                price_at_purchase=item[1].price,
                quantity=item[0].quantity,
            )
            await self.cart_repository.delete_cart_item(item[0].id)
        return order

    async def get_order_by_id(
        self, order_id: int, user_id: int
    ) -> tuple[OrderModel, list[OrderItemModel]]:
        order = await self.order_repository.get_order_by_id(order_id)
        if not order or order[0].user_id != user_id:
            raise OrderNotFoundError(order_id)
        return order
