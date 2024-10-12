import uuid
from enum import Enum
from sqlalchemy import Column, Integer, String, UUID, Enum as EnumColumn, LargeBinary, DateTime
from app.core.db import database
from datetime import datetime


class KeyType(str, Enum):
    access_token = "ACCESS_TOKEN"
    refresh_token = "REFRESH_TOKEN"
    verification_token = "VERIFICATION_TOKEN"
    reset_password_token = "RESET_PASSWORD_TOKEN"


class Key(database.Base):
    __tablename__ = "keys"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    key_type = Column(EnumColumn(KeyType))
    public_key = Column(String)
    hashed_private_key = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    deleted_at = Column(DateTime, nullable=True)
