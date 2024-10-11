from sqlalchemy.orm import Session
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
