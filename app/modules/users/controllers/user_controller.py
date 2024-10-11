from fastapi import APIRouter, Depends
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
