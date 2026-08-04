from typing import Sequence

from app.models.cartItemModel import CartModel
from app.repositories.cartRepository import CartRepository
from app.repositories.orderRepository import OrderRepository
from app.repositories.productRepository import ProductRepository


class OrderService:
    order_repository: OrderRepository
    cart_repository: CartRepository
    product_repository: ProductRepository

    def __init__(
        self,
        order_repository: OrderRepository,
        cart_repository: CartRepository,
        product_repository: ProductRepository,
    ):
        self.order_repository = order_repository
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    
