from decimal import Decimal
from typing import Optional, Sequence

from sqlalchemy import Row, select

from app.db.database import AsyncSession
from app.models.orderModel import OrderModel, OrderItemModel


class OrderRepository:
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_order(self, user_id: int) -> OrderModel:
        order = OrderModel(user_id=user_id)
        self.session.add(order)
        await self.session.flush()
        return order

    async def add_order_item(
        self,
        order_id: int,
        product_id: int,
        product_name: str,
        price_at_purchase: Decimal,
        quantity: int,
    ) -> OrderItemModel:
        order_item = OrderItemModel(
            order_id=order_id,
            product_id=product_id,
            product_name=product_name,
            price_at_purchase=price_at_purchase,
            quantity=quantity,
        )
        self.session.add(order_item)
        return order_item

    async def get_order_by_id(
        self, order_id: int
    ) -> Optional[tuple[OrderModel, list[OrderItemModel]]]:
        stmt = (
            select(OrderItemModel, OrderModel)
            .join(OrderModel, OrderModel.id == OrderItemModel.order_id)
            .where(OrderModel.id == order_id)
        )
        response = await self.session.execute(stmt)
        rows = response.all()
        if not rows:
            return None
        grouped: tuple[OrderModel, list[OrderItemModel]] = (rows[0][1], [])
        for order_item, order in rows:
            grouped[1].append(order_item)
        return grouped

    async def get_orders_by_user_id(
        self, user_id: int
    ) -> list[tuple[OrderModel, list[OrderItemModel]]]:
        stmt = (
            select(OrderItemModel, OrderModel)
            .join(OrderModel, OrderModel.id == OrderItemModel.order_id)
            .where(OrderModel.user_id == user_id)
        )
        response = await self.session.execute(stmt)
        rows = response.all()

        grouped: dict[int, tuple[OrderModel, list[OrderItemModel]]] = {}

        for order_item, order in rows:
            if order.id not in grouped:
                grouped[order.id] = (order, [])
            grouped[order.id][1].append(order_item)

        return list(grouped.values())
