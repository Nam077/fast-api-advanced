from pydantic import BaseModel
from uuid import UUID

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID  # Đảm bảo đây là kiểu UUID

    class Config:
        from_attributes = True
