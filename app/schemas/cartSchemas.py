from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CartItemResponseSchema(BaseModel):
    id: int
    product_id: int
    product_name: str
    price: Decimal = Field(gt=0)
    quantity: int = Field(gt=0)
    subtotal: Decimal = Field(gt=0)


class CartAddSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    quantity: int = Field(gt=0)


class CartAddResponseSchema(CartAddSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
