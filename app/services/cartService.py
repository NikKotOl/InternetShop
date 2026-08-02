from app.core.exceptions import InvalidQuantityError, ProductNotFoundError
from app.models.cartItemModel import CartModel
from app.repositories.cartRepository import CartRepository
from app.repositories.productRepository import ProductRepository


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
