from sqlalchemy.orm import Session

from app.modules.keys.models.key_model import KeyType
from app.modules.keys.repositories.key_repository import KeyRepository


class KeyService:
    def __init__(self):
        self.key_repo = KeyRepository()

    def get_keys(self, db: Session):
        return self.key_repo.get_all(db)

    def get_key_by_key_type(self, db: Session):
        return self.key_repo.get_key_by_type(db, key_type=KeyType.refresh_token)

    def auto_key_rotation(self, db: Session):
        return self.key_repo.auto_key_rotation(db)
