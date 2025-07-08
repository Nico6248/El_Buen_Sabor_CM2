from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy import and_

from src.menu.domain.menu_repository import MenuRepository
from src.menu.domain.menu_model import Dish, DishCreate

class MenuRepositoryDB(MenuRepository):
    """Implementación del repositorio de menú usando PostgreSQL"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, dish: DishCreate) -> Dish:
        """Crea un nuevo plato"""
        db_dish = Dish.from_orm(dish)
        self.session.add(db_dish)
        self.session.commit()
        self.session.refresh(db_dish)
        return db_dish
    
    def get_by_id(self, dish_id: int) -> Optional[Dish]:
        """Obtiene un plato por ID"""
        return self.session.get(Dish, dish_id)
    
    def get_by_restaurant(self, restaurant_id: int, available_only: bool = True) -> List[Dish]:
        """Obtiene todos los platos de un restaurante"""
        query = select(Dish).where(Dish.restaurant_id == restaurant_id)
        if available_only:
            query = query.where(Dish.is_available == True)
        return self.session.exec(query).all()
    
    def get_all(self) -> List[Dish]:
        """Obtiene todos los platos"""
        return self.session.exec(select(Dish)).all()
    
    def update(self, dish_id: int, dish_data: DishCreate) -> Optional[Dish]:
        """Actualiza un plato"""
        dish = self.session.get(Dish, dish_id)
        if not dish:
            return None
        
        # Actualizar campos
        dish.name = dish_data.name
        dish.description = dish_data.description
        dish.category = dish_data.category
        dish.restaurant_id = dish_data.restaurant_id
        dish.is_available = dish_data.is_available
        
        self.session.commit()
        self.session.refresh(dish)
        return dish
    
    def delete(self, dish_id: int) -> bool:
        """Elimina un plato"""
        dish = self.session.get(Dish, dish_id)
        if not dish:
            return False
        
        self.session.delete(dish)
        self.session.commit()
        return True
    
    def exists_by_name_and_restaurant(self, name: str, restaurant_id: int) -> bool:
        """Verifica si existe un plato con el mismo nombre en el restaurante"""
        existing_dish = self.session.exec(
            select(Dish).where(
                and_(Dish.restaurant_id == restaurant_id, Dish.name == name)
            )
        ).first()
        return existing_dish is not None 