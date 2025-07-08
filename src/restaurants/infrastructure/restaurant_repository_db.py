from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy import and_

from src.restaurants.domain.restaurant_repository import RestaurantRepository
from src.restaurants.domain.restaurant_model import Restaurant, RestaurantCreate, Table, TableCreate

class RestaurantRepositoryDB(RestaurantRepository):
    """Implementación del repositorio de restaurantes usando PostgreSQL"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_restaurant(self, restaurant: RestaurantCreate) -> Restaurant:
        """Crea un nuevo restaurante"""
        db_restaurant = Restaurant.from_orm(restaurant)
        self.session.add(db_restaurant)
        self.session.commit()
        self.session.refresh(db_restaurant)
        return db_restaurant
    
    def get_restaurant_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        """Obtiene un restaurante por ID"""
        return self.session.get(Restaurant, restaurant_id)
    
    def get_all_restaurants(self) -> List[Restaurant]:
        """Obtiene todos los restaurantes"""
        return self.session.exec(select(Restaurant)).all()
    
    def update_restaurant(self, restaurant_id: int, restaurant_data: RestaurantCreate) -> Optional[Restaurant]:
        """Actualiza un restaurante"""
        restaurant = self.session.get(Restaurant, restaurant_id)
        if not restaurant:
            return None
        
        # Actualizar campos
        restaurant.name = restaurant_data.name
        restaurant.location = restaurant_data.location
        restaurant.opening_time = restaurant_data.opening_time
        restaurant.closing_time = restaurant_data.closing_time
        
        self.session.commit()
        self.session.refresh(restaurant)
        return restaurant
    
    def delete_restaurant(self, restaurant_id: int) -> bool:
        """Elimina un restaurante"""
        restaurant = self.session.get(Restaurant, restaurant_id)
        if not restaurant:
            return False
        
        self.session.delete(restaurant)
        self.session.commit()
        return True
    
    def create_table(self, table: TableCreate) -> Table:
        """Crea una nueva mesa"""
        db_table = Table.from_orm(table)
        self.session.add(db_table)
        self.session.commit()
        self.session.refresh(db_table)
        return db_table
    
    def get_table_by_id(self, table_id: int) -> Optional[Table]:
        """Obtiene una mesa por ID"""
        return self.session.get(Table, table_id)
    
    def get_tables_by_restaurant(self, restaurant_id: int) -> List[Table]:
        """Obtiene todas las mesas de un restaurante"""
        return self.session.exec(
            select(Table).where(Table.restaurant_id == restaurant_id)
        ).all()
    
    def update_table(self, table_id: int, table_data: TableCreate) -> Optional[Table]:
        """Actualiza una mesa"""
        table = self.session.get(Table, table_id)
        if not table:
            return None
        
        # Actualizar campos
        table.table_number = table_data.table_number
        table.capacity = table_data.capacity
        table.location_in_restaurant = table_data.location_in_restaurant
        table.restaurant_id = table_data.restaurant_id
        
        self.session.commit()
        self.session.refresh(table)
        return table
    
    def delete_table(self, table_id: int) -> bool:
        """Elimina una mesa"""
        table = self.session.get(Table, table_id)
        if not table:
            return False
        
        self.session.delete(table)
        self.session.commit()
        return True
    
    def exists_table_number_in_restaurant(self, table_number: int, restaurant_id: int) -> bool:
        """Verifica si existe una mesa con el mismo número en el restaurante"""
        existing_table = self.session.exec(
            select(Table).where(
                and_(Table.restaurant_id == restaurant_id, Table.table_number == table_number)
            )
        ).first()
        return existing_table is not None 