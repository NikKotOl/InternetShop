from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CategoryCreateSchema(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )



class CategoryResponseSchema(CategoryCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    # created_at: datetime
    # updated_at: datetime
