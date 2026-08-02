from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100, pattern=r"\S+")

    category_id: int
    price: Decimal = Field(gt=0)


class ProductResponseSchema(ProductCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
