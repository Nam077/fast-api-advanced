import uuid

from sqlalchemy import Column, Integer, String, UUID
from app.core.db import database


class User(database.Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
