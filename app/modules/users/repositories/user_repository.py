from sqlalchemy import cast
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.modules.users.models.user_model import User
from fastapi import HTTPException
from typing import List, Optional, Type
from uuid import UUID
from app.core.repositories.base_repository import BaseRepositoryInterface


class UserRepository(BaseRepositoryInterface[User, UUID]):

    def get_all(self, db: Session) -> list[Type[User]]:
        try:
            return db.query(User).all()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def get_by_id(self, db: Session, entity_id: UUID) -> Optional[User]:
        try:
            return db.query(User).filter(User.id == entity_id).first()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def create(self, db: Session, entity: User) -> User:
        try:
            if self.get_user_by_username(db, entity.username):
                raise HTTPException(status_code=400, detail="Username is already taken")
            db.add(entity)
            db.commit()
            db.refresh(entity)
            return entity
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def update(self, db: Session, entity_id: UUID, entity: User) -> Optional[User]:
        try:
            existing_user = self.get_by_id(db, entity_id)
            if not existing_user:
                raise HTTPException(status_code=404, detail="User not found")
            # Giả sử chúng ta chỉ cập nhật username
            existing_user.username = entity.username
            db.commit()
            db.refresh(existing_user)
            return existing_user
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def delete(self, db: Session, entity_id: UUID) -> bool:
        try:
            user = self.get_by_id(db, entity_id)
            if not user:
                return False
            db.delete(user)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        try:
            return db.query(User).filter(User.username == username).first()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
