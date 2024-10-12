from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.modules.keys.schemas.key_schemas import KeySchema
from app.modules.keys.services.key_service import KeyService
from app.modules.users.schemas.user_schema import UserCreate, UserResponse
from app.modules.users.services.user_service import UserService
from app.core.db import database
from app.core.security import verify_token  # Bạn sẽ cần hàm này để kiểm tra token
from uuid import UUID
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserController:
    def __init__(self):
        self.router = APIRouter()
        self.user_service = UserService()
        self.key_service = KeyService()
        self._register_routes()

    def _register_routes(self):
        @self.router.get("/users/", response_model=List[UserResponse])
        async def get_users(db: Session = Depends(database.get_db)):
            print(settings.MASTER_KEY)
            return self.user_service.get_users(db)

        @self.router.get("/users/{user_id}", response_model=UserResponse)
        async def get_user_by_id(user_id: UUID, token: str = Depends(oauth2_scheme),
                                 db: Session = Depends(database.get_db)):
            current_user = verify_token(token)
            if not current_user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            return self.user_service.get_user_by_id(db, user_id)

        @self.router.post("/users/", response_model=UserResponse)
        async def create_user(user_create: UserCreate, token: str = Depends(oauth2_scheme),
                              db: Session = Depends(database.get_db)):
            current_user = verify_token(token)
            if not current_user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            return self.user_service.create_user(db, user_create)

        @self.router.get("/test/", response_model=KeySchema)
        async def get_keys(db: Session = Depends(database.get_db)):
            return self.key_service.get_key_by_key_type(db)
