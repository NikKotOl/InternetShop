from decimal import Decimal

from pydantic import BaseModel, Field


class CartItemResponseSchema(BaseModel):
    id: int
    product_id: int
    product_name: str
    price: Decimal = Field(gt=0)
    quantity: int = Field(gt=0)
    subtotal: Decimal = Field(gt=0)
