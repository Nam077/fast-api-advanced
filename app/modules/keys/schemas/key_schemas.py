from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.modules.keys.models.key_model import KeyType


class KeySchema(BaseModel):
    id: UUID
    key_type: KeyType
    public_key: str
    private_key: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None

    class Config:
        from_attributes = True
