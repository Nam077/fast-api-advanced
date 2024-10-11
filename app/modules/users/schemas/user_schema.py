from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.v1 import UUID4


class UserBase(BaseModel):
    username: str = Field(
       ...,
        description="The unique username for the user. Must be between 3 and 20 characters.",
        min_length=3,
        max_length=20,
        examples=["JohnDoe"]
    )


class UserCreate(UserBase):
    password: str = Field(
        ...,
        description="The password for the user. Must be at least 8 characters.",
        min_length=8,
        examples=["Password123"],

    )
    


class UserResponse(UserBase):

    id: UUID = Field(
        ...,
        description="The unique identifier for the user.",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    class Config:
        from_attributes = True
