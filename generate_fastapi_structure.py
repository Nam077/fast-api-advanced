import os

# Danh sách các thư mục cần tạo
folders = [
    "app",
    "app/modules",
    "app/modules/users/controllers",
    "app/modules/users/services",
    "app/modules/users/repositories",
    "app/modules/users/schemas",
    "app/modules/users/models",
    "app/core",
    "app/tests"
]

# Các file cần tạo và nội dung mặc định
files = {
    "app/main.py": '''from app.core.application import Application

# Khởi tạo và chạy ứng dụng FastAPI
app = Application().get_app()
''',
    "app/core/application.py": '''from fastapi import FastAPI
from app.modules.users.controllers.user_controller import UserController

class Application:
    def __init__(self):
        self.app = FastAPI()
        self._register_controllers()

    def _register_controllers(self):
        user_controller = UserController()
        self.app.include_router(user_controller.router)

    def get_app(self):
        return self.app
''',
    "app/core/config.py": '''from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Class-Based App"
    DATABASE_URL: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"

settings = Settings()
''',
    "app/core/db.py": '''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

class Database:
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
        self.engine = create_engine(self.SQLALCHEMY_DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

database = Database()
''',
    "app/core/security.py": '''from passlib.context import CryptContext

class Security:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

security = Security()
''',
    "app/modules/users/controllers/user_controller.py": '''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.modules.users.schemas.user_schema import UserCreate, User
from app.modules.users.services.user_service import UserService
from app.core.db import database

class UserController:
    def __init__(self):
        self.router = APIRouter()
        self.user_service = UserService()
        self._register_routes()

    def _register_routes(self):
        @self.router.get("/users/", response_model=list[User])
        async def get_users(db: Session = Depends(database.get_db)):
            return self.user_service.get_users(db)

        @self.router.post("/users/", response_model=User)
        async def create_user(user_create: UserCreate, db: Session = Depends(database.get_db)):
            return self.user_service.create_user(db, user_create)
''',
    "app/modules/users/models/user_model.py": '''from sqlalchemy import Column, Integer, String
from app.core.db import database

class User(database.Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
''',
    "app/modules/users/schemas/user_schema.py": '''from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True  # Thay orm_mode thành from_attributes cho Pydantic v2
''',
    "app/modules/users/repositories/user_repository.py": '''from sqlalchemy.orm import Session
from app.modules.users.models.user_model import User

class UserRepository:
    def get_users(self, db: Session):
        return db.query(User).all()

    def get_user_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    def create_user(self, db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
''',
    "app/modules/users/services/user_service.py": '''from sqlalchemy.orm import Session
from app.modules.users.repositories.user_repository import UserRepository
from app.modules.users.schemas.user_schema import UserCreate
from app.core.security import security
from app.modules.users.models.user_model import User

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_users(self, db: Session):
        return self.user_repository.get_users(db)

    def create_user(self, db: Session, user_create: UserCreate):
        hashed_password = security.get_password_hash(user_create.password)
        user = User(username=user_create.username, hashed_password=hashed_password)
        return self.user_repository.create_user(db, user)
''',
    "app/__init__.py": "",
    "app/core/__init__.py": "",
    "app/modules/__init__.py": "",
    "app/modules/users/__init__.py": "",
    "app/tests/__init__.py": "",
    ".env": "DATABASE_URL=sqlite:///./test.db\n"
}

# Hàm tạo các thư mục
def create_folders():
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {folder}")

# Hàm tạo các file
def create_files():
    for file_path, content in files.items():
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Created file: {file_path}")

if __name__ == "__main__":
    create_folders()
    create_files()
    print("Project structure has been created successfully.")
