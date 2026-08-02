from typing import Optional, Sequence

from sqlalchemy import Row, select

from app.models.cartItemModel import CartModel
from app.db.database import AsyncSession
from app.models.productModel import ProductModel


class CartRepository:
    session: AsyncSession

    def __init__(self, session):
        self.session = session

    async def add_cart(self, user_id: int, product_id: int, quantity: int) -> CartModel:
        new_cart = CartModel(user_id=user_id, product_id=product_id, quantity=quantity)
        self.session.add(new_cart)
        await self.session.commit()
        await self.session.refresh(new_cart)
        return new_cart

    async def quantity_update(self, cart: CartModel, quantity: int) -> CartModel:
        cart.quantity = quantity
        await self.session.commit()
        await self.session.refresh(cart)
        return cart

    async def delete_cart_item(self, id: int) -> Optional[CartModel]:
        cart = await self.session.get(CartModel, id)
        if not cart:
            return None
        await self.session.delete(cart)
        await self.session.commit()
        return cart

    async def get_carts_by_user_id(self, user_id: int) -> Sequence[CartModel]:
        stmt = select(CartModel).where(CartModel.user_id == user_id)
        carts = await self.session.execute(stmt)
        return carts.scalars().all()

    async def get_cart_item_by_user_and_product(
        self, user_id: int, product_id: int
    ) -> Optional[CartModel]:
        stmt = select(CartModel).where(
            CartModel.user_id == user_id, CartModel.product_id == product_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_cart_items_with_products_by_user_id(
        self, user_id: int
    ) -> Sequence[Row[tuple[CartModel, ProductModel]]]:
        stmt = (
            select(CartModel, ProductModel)
            .join(ProductModel, CartModel.product_id == ProductModel.id)
            .where(CartModel.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.all()
