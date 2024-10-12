from datetime import timedelta, datetime
from typing import Type, Optional, cast
from uuid import UUID
from sqlalchemy import cast, Enum as EnumColumn, desc
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.db import database
from app.core.repositories.base_repository import BaseRepositoryInterface
from app.core.security import security
from app.modules.keys.models.key_model import Key, KeyType
from app.core.config import settings
from app.modules.keys.schemas.key_schemas import KeySchema


class KeyRepository(BaseRepositoryInterface[Key, UUID]):

    def get_all(self, db: Session) -> list[Type[Key]]:
        try:
            return db.query(Key).all()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def get_by_id(self, db: Session, entity_id: UUID) -> Optional[Key]:
        try:
            return db.query(Key).filter(Key.id == entity_id).first()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def create(self, db: Session, entity: Key) -> Key:
        try:
            db.add(entity)
            db.commit()
            db.refresh(entity)
            return entity
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def update(self, db: Session, entity_id: UUID, entity: Key) -> Optional[Key]:
        try:
            existing_key = self.get_by_id(db, entity_id)
            if not existing_key:
                raise HTTPException(status_code=404, detail="Key not found")
            # Giả sử chúng ta chỉ cập nhật key_type
            existing_key.key_type = entity.key_type
            db.commit()
            db.refresh(existing_key)
            return existing_key
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def delete(self, db: Session, entity_id: UUID) -> bool:
        try:
            key = self.get_by_id(db, entity_id)
            if not key:
                return False
            db.delete(key)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def get_key_by_type(self, db: Session, key_type: KeyType) -> str:
        try:
            # Kiểm tra nếu có key theo loại đã tồn tại hay không
            key = (
                db.query(Key)
                .filter(cast(Key.key_type, EnumColumn(KeyType)) == key_type)
                .order_by(desc(cast(Key.created_at, KeyType)))
                .first()  # Lấy bản ghi đầu tiên (mới nhất)
            )

            # Nếu không có key, tạo mới một key
            if not key:
                key = self.generate_key(db, key_type)
            # xoá encrypted private key
            key.private_key = security.decrypt_private_key(key.hashed_private_key, settings.MASTER_KEY)
            return key
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def generate_key(self, db: Session, key_type: KeyType) -> KeySchema:
        try:
            private_key, public_key = security.generate_rsa_key_pair()
            try:
                hashed_private_key = security.encrypt_private_key(private_key, settings.MASTER_KEY)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error decrypting private key: {str(e)}")

            # Tạo bản ghi mới với public_key và hashed_private_key
            key = Key(public_key=public_key, hashed_private_key=hashed_private_key, key_type=key_type)

            # Lưu key mới vào cơ sở dữ liệu
            return self.create(db, key)
        except SQLAlchemyError as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def delete_old_keys(self, db: Session, days: int, key_type: KeyType):
        threshold_date = datetime.now() - timedelta(days=days)
        try:
            db.query(Key).filter(Key.created_at < threshold_date, Key.key_type == key_type).delete(
                synchronize_session=False)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def auto_key_rotation(self, db):
        # Xoá các key cũ
        self.delete_old_keys(db, 30, KeyType.access_token)
        self.delete_old_keys(db, 30, KeyType.refresh_token)
        self.delete_old_keys(db, 30, KeyType.verification_token)
        self.delete_old_keys(db, 30, KeyType.reset_password_token)

        # Tạo key mới
        self.generate_key(db, KeyType.access_token)
        self.generate_key(db, KeyType.refresh_token)
        self.generate_key(db, KeyType.verification_token)
        self.generate_key(db, KeyType.reset_password_token)
        print("Key rotation completed")
        return True
