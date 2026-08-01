from pydantic import BaseModel, ConfigDict, Field


class UserSchema(BaseModel):
    username: str = Field(min_length=1, max_length=100, pattern=r"\S+")


class UserCreateSchema(UserSchema):
    password: str = Field(min_length=1, max_length=100, pattern=r"\S+")


class UserResponseSchema(UserSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserLoginSchema(UserSchema):
    password: str = Field(min_length=1, max_length=100, pattern=r"\S+")
