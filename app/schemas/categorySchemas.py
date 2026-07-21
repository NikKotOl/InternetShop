from pydantic import BaseModel, Field, ConfigDict


class CategoryCreateSchema(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
        pattern=r'\S+'
    )



class CategoryResponseSchema(CategoryCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    # created_at: datetime
    # updated_at: datetime
