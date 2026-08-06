from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, computed_field


class OrderItemResponseSchema(BaseModel):
    product_name: str
    price_at_purchase: Decimal
    quantity: int

    class Config:
        from_attributes = True


class OrderResponseSchema(BaseModel):
    id: int
    created_at: datetime
    items: list[OrderItemResponseSchema]

    @computed_field
    @property
    def total_price(self) -> Decimal:
        return sum(
            (item.price_at_purchase * item.quantity for item in self.items),
            start=Decimal("0"),
        )

    class Config:
        from_attributes = True
