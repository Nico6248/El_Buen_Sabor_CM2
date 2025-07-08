from abc import ABC, abstractmethod
from typing import List, Optional
from .menu_model import Dish, DishCreate, DishRead

class MenuRepository(ABC):
    """Repositorio abstracto para gestión del menú"""
    
    @abstractmethod
    def create(self, dish: DishCreate) -> Dish:
        """Crea un nuevo plato"""
        pass
    
    @abstractmethod
    def get_by_id(self, dish_id: int) -> Optional[Dish]:
        """Obtiene un plato por ID"""
        pass
    
    @abstractmethod
    def get_by_restaurant(self, restaurant_id: int, available_only: bool = True) -> List[Dish]:
        """Obtiene todos los platos de un restaurante"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Dish]:
        """Obtiene todos los platos"""
        pass
    
    @abstractmethod
    def update(self, dish_id: int, dish_data: DishCreate) -> Optional[Dish]:
        """Actualiza un plato"""
        pass
    
    @abstractmethod
    def delete(self, dish_id: int) -> bool:
        """Elimina un plato"""
        pass
    
    @abstractmethod
    def exists_by_name_and_restaurant(self, name: str, restaurant_id: int) -> bool:
        """Verifica si existe un plato con el mismo nombre en el restaurante"""
        pass 