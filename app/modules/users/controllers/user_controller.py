from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.modules.users.schemas.user_schema import UserCreate, UserResponse
from app.modules.users.services.user_service import UserService
from app.core.db import database
from uuid import UUID


class UserController:
    def __init__(self):
        self.router = APIRouter()
        self.user_service = UserService()
        self._register_routes()

    def _register_routes(self):
        @self.router.get("/users/", response_model=List[UserResponse])
        async def get_users(db: Session = Depends(database.get_db)):
            return self.user_service.get_users(db)

        # find by id
        @self.router.get("/users/{id:uuid}", response_model=UserResponse, description="Find user by id ok")
        async def get_user_by_id(id: UUID, db: Session = Depends(database.get_db)):
            return self.user_service.get_user_by_id(db, id)


        @self.router.post("/users/", response_model=UserResponse)
        async def create_user(user_create: UserCreate, db: Session = Depends(database.get_db)):
            return self.user_service.create_user(db, user_create)
