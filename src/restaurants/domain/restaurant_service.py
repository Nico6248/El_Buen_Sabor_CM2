from typing import List, Optional
from .restaurant_repository import RestaurantRepository
from .restaurant_model import Restaurant, RestaurantCreate, Table, TableCreate

class RestaurantService:
    """Servicio de aplicación para gestión de restaurantes"""
    
    def __init__(self, repository: RestaurantRepository):
        self.repository = repository
    
    def create_restaurant(self, restaurant: RestaurantCreate) -> Restaurant:
        """Crea un nuevo restaurante con validaciones de negocio"""
        # Validar horarios
        if restaurant.closing_time <= restaurant.opening_time:
            raise ValueError("La hora de cierre debe ser posterior a la de apertura")
        
        return self.repository.create_restaurant(restaurant)
    
    def get_restaurant_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        """Obtiene un restaurante por ID"""
        return self.repository.get_restaurant_by_id(restaurant_id)
    
    def get_all_restaurants(self) -> List[Restaurant]:
        """Obtiene todos los restaurantes"""
        return self.repository.get_all_restaurants()
    
    def update_restaurant(self, restaurant_id: int, restaurant_data: RestaurantCreate) -> Optional[Restaurant]:
        """Actualiza un restaurante con validaciones"""
        # Validar que el restaurante existe
        existing_restaurant = self.repository.get_restaurant_by_id(restaurant_id)
        if not existing_restaurant:
            raise ValueError("Restaurante no encontrado")
        
        # Validar horarios
        if restaurant_data.closing_time <= restaurant_data.opening_time:
            raise ValueError("La hora de cierre debe ser posterior a la de apertura")
        
        return self.repository.update_restaurant(restaurant_id, restaurant_data)
    
    def delete_restaurant(self, restaurant_id: int) -> bool:
        """Elimina un restaurante"""
        existing_restaurant = self.repository.get_restaurant_by_id(restaurant_id)
        if not existing_restaurant:
            raise ValueError("Restaurante no encontrado")
        
        return self.repository.delete_restaurant(restaurant_id)
    
    def create_table(self, table: TableCreate) -> Table:
        """Crea una nueva mesa con validaciones de negocio"""
        # Validar que el restaurante existe
        restaurant = self.repository.get_restaurant_by_id(table.restaurant_id)
        if not restaurant:
            raise ValueError("Restaurante no encontrado")
        
        # Validar capacidad de mesa
        if table.capacity < 2 or table.capacity > 12:
            raise ValueError("La capacidad de la mesa debe estar entre 2 y 12 personas")
        
        # Validar que el número de mesa no se repita
        if self.repository.exists_table_number_in_restaurant(table.table_number, table.restaurant_id):
            raise ValueError("El número de mesa ya existe en este restaurante")
        
        return self.repository.create_table(table)
    
    def get_table_by_id(self, table_id: int) -> Optional[Table]:
        """Obtiene una mesa por ID"""
        return self.repository.get_table_by_id(table_id)
    
    def get_tables_by_restaurant(self, restaurant_id: int) -> List[Table]:
        """Obtiene todas las mesas de un restaurante"""
        # Validar que el restaurante existe
        restaurant = self.repository.get_restaurant_by_id(restaurant_id)
        if not restaurant:
            raise ValueError("Restaurante no encontrado")
        
        tables = self.repository.get_tables_by_restaurant(restaurant_id)
        if not tables:
            raise ValueError("No se encontraron mesas para este restaurante")
        
        return tables
    
    def update_table(self, table_id: int, table_data: TableCreate) -> Optional[Table]:
        """Actualiza una mesa con validaciones"""
        # Validar que la mesa existe
        existing_table = self.repository.get_table_by_id(table_id)
        if not existing_table:
            raise ValueError("Mesa no encontrada")
        
        # Validar que el restaurante existe
        restaurant = self.repository.get_restaurant_by_id(table_data.restaurant_id)
        if not restaurant:
            raise ValueError("Restaurante no encontrado")
        
        # Validar capacidad de mesa
        if table_data.capacity < 2 or table_data.capacity > 12:
            raise ValueError("La capacidad de la mesa debe estar entre 2 y 12 personas")
        
        # Validar que el número de mesa no se repita (excluyendo la mesa actual)
        if (table_data.table_number != existing_table.table_number and 
            self.repository.exists_table_number_in_restaurant(table_data.table_number, table_data.restaurant_id)):
            raise ValueError("El número de mesa ya existe en este restaurante")
        
        return self.repository.update_table(table_id, table_data)
    
    def delete_table(self, table_id: int) -> bool:
        """Elimina una mesa"""
        existing_table = self.repository.get_table_by_id(table_id)
        if not existing_table:
            raise ValueError("Mesa no encontrada")
        
        return self.repository.delete_table(table_id) 