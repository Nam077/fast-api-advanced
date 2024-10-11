from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

# T represents the type of the entity (e.g., User, Product)
T = TypeVar('T')
ID = TypeVar('ID')

class BaseRepositoryInterface(ABC, Generic[T, ID]):
    
    @abstractmethod
    def get_all(self, db) -> List[T]:
        """Lấy tất cả các bản ghi"""
        pass

    @abstractmethod
    def get_by_id(self, db, entity_id: ID) -> Optional[T]:
        """Lấy bản ghi theo ID"""
        pass

    @abstractmethod
    def create(self, db, entity: T) -> T:
        """Tạo mới một bản ghi"""
        pass

    @abstractmethod
    def update(self, db, entity_id: ID, entity: T) -> Optional[T]:
        """Cập nhật một bản ghi dựa trên ID"""
        pass

    @abstractmethod
    def delete(self, db, entity_id: ID) -> bool:
        """Xóa một bản ghi dựa trên ID"""
        pass
