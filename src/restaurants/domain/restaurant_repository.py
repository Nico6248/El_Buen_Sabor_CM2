from abc import ABC, abstractmethod
from typing import List, Optional
from .restaurant_model import Restaurant, RestaurantCreate, Table, TableCreate

class RestaurantRepository(ABC):
    """Repositorio abstracto para gestión de restaurantes"""
    
    @abstractmethod
    def create_restaurant(self, restaurant: RestaurantCreate) -> Restaurant:
        """Crea un nuevo restaurante"""
        pass
    
    @abstractmethod
    def get_restaurant_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        """Obtiene un restaurante por ID"""
        pass
    
    @abstractmethod
    def get_all_restaurants(self) -> List[Restaurant]:
        """Obtiene todos los restaurantes"""
        pass
    
    @abstractmethod
    def update_restaurant(self, restaurant_id: int, restaurant_data: RestaurantCreate) -> Optional[Restaurant]:
        """Actualiza un restaurante"""
        pass
    
    @abstractmethod
    def delete_restaurant(self, restaurant_id: int) -> bool:
        """Elimina un restaurante"""
        pass
    
    @abstractmethod
    def create_table(self, table: TableCreate) -> Table:
        """Crea una nueva mesa"""
        pass
    
    @abstractmethod
    def get_table_by_id(self, table_id: int) -> Optional[Table]:
        """Obtiene una mesa por ID"""
        pass
    
    @abstractmethod
    def get_tables_by_restaurant(self, restaurant_id: int) -> List[Table]:
        """Obtiene todas las mesas de un restaurante"""
        pass
    
    @abstractmethod
    def update_table(self, table_id: int, table_data: TableCreate) -> Optional[Table]:
        """Actualiza una mesa"""
        pass
    
    @abstractmethod
    def delete_table(self, table_id: int) -> bool:
        """Elimina una mesa"""
        pass
    
    @abstractmethod
    def exists_table_number_in_restaurant(self, table_number: int, restaurant_id: int) -> bool:
        """Verifica si existe una mesa con el mismo número en el restaurante"""
        pass 