# app/core/db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

class Database:
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
        self.engine = create_engine(self.SQLALCHEMY_DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def create_tables(self):
        # Import các model trước khi tạo bảng
        from app.modules.users.models.user_model import User
        self.Base.metadata.create_all(bind=self.engine)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

database = Database()
