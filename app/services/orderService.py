from app.repositories.orderRepository import OrderRepository


class OrderService:
    order_repository: OrderRepository

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
