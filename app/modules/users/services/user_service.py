from sqlalchemy.orm import Session
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
