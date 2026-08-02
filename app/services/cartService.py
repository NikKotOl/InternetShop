from typing import Sequence

from app.core.exceptions import InvalidQuantityError, ProductNotFoundError
from app.models.cartItemModel import CartModel
from app.repositories.cartRepository import CartRepository
from app.repositories.productRepository import ProductRepository
from app.schemas.cartSchemas import CartItemResponseSchema


class CartService:
    cart_repository: CartRepository
    product_repository: ProductRepository

    def __init__(
        self, cart_repository: CartRepository, product_repository: ProductRepository
    ):
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    async def add_to_cart(
        self, user_id: int, product_id: int, quantity: int
    ) -> CartModel:
        cart = await self.cart_repository.get_cart_item_by_user_and_product(
            user_id=user_id, product_id=product_id
        )
        if quantity < 1:
            raise InvalidQuantityError(quantity)
        if cart is not None:
            await self.cart_repository.quantity_update(
                cart=cart, quantity=cart.quantity + quantity
            )
            return cart
        product = await self.product_repository.get_product_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return await self.cart_repository.add_cart(
            user_id=user_id, product_id=product_id, quantity=quantity
        )

    async def get_user_cart(self, user_id: int) -> Sequence[CartItemResponseSchema]:
        carts_row = await self.cart_repository.get_cart_items_with_products_by_user_id(
            user_id
        )
        schemas = []
        for cart_item, product in carts_row:
            schema = CartItemResponseSchema(
                id=cart_item.id,
                product_id=product.id,
                product_name=product.name,
                price=product.price,
                quantity=cart_item.quantity,
                subtotal=cart_item.price * cart_item.quantity,
            )
            schemas.append(schema)
        return schemas
