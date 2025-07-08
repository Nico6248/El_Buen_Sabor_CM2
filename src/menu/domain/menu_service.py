from typing import List, Optional
from .menu_repository import MenuRepository
from .menu_model import Dish, DishCreate, DishRead, DishCategory
from src.restaurants.domain.restaurant_model import Restaurant

class MenuService:
    """Servicio de aplicación para gestión del menú"""
    
    def __init__(self, repository: MenuRepository):
        self.repository = repository
    
    def create_dish(self, dish: DishCreate, restaurant_exists: bool) -> Dish:
        """Crea un nuevo plato con validaciones de negocio"""
        # Validar categoría
        valid_categories = [DishCategory.ENTRADA, DishCategory.PRINCIPAL, DishCategory.POSTRE, DishCategory.BEBIDA]
        if dish.category not in valid_categories:
            raise ValueError(f"Categoría inválida. Use una de: {valid_categories}")
        
        # Validar que el restaurante existe
        if not restaurant_exists:
            raise ValueError("Restaurante no encontrado")
        
        # Validar que el nombre del plato es único en el restaurante
        if self.repository.exists_by_name_and_restaurant(dish.name, dish.restaurant_id):
            raise ValueError("Ya existe un plato con este nombre en el restaurante")
        
        return self.repository.create(dish)
    
    def get_dish_by_id(self, dish_id: int) -> Optional[Dish]:
        """Obtiene un plato por ID"""
        return self.repository.get_by_id(dish_id)
    
    def get_menu_for_restaurant(self, restaurant_id: int, available_only: bool = True) -> List[Dish]:
        """Obtiene el menú de un restaurante"""
        dishes = self.repository.get_by_restaurant(restaurant_id, available_only)
        if not dishes:
            raise ValueError("No se encontró menú para este restaurante")
        return dishes
    
    def get_all_dishes(self) -> List[Dish]:
        """Obtiene todos los platos"""
        return self.repository.get_all()
    
    def update_dish(self, dish_id: int, dish_data: DishCreate, restaurant_exists: bool) -> Optional[Dish]:
        """Actualiza un plato con validaciones"""
        # Validar que el plato existe
        existing_dish = self.repository.get_by_id(dish_id)
        if not existing_dish:
            raise ValueError("Plato no encontrado")
        
        # Validar categoría
        valid_categories = [DishCategory.ENTRADA, DishCategory.PRINCIPAL, DishCategory.POSTRE, DishCategory.BEBIDA]
        if dish_data.category not in valid_categories:
            raise ValueError(f"Categoría inválida. Use una de: {valid_categories}")
        
        # Validar que el restaurante existe
        if not restaurant_exists:
            raise ValueError("Restaurante no encontrado")
        
        # Validar que el nombre del plato es único (excluyendo el plato actual)
        if (dish_data.name != existing_dish.name and 
            self.repository.exists_by_name_and_restaurant(dish_data.name, dish_data.restaurant_id)):
            raise ValueError("Ya existe un plato con este nombre en el restaurante")
        
        return self.repository.update(dish_id, dish_data)
    
    def delete_dish(self, dish_id: int) -> bool:
        """Elimina un plato"""
        existing_dish = self.repository.get_by_id(dish_id)
        if not existing_dish:
            raise ValueError("Plato no encontrado")
        
        return self.repository.delete(dish_id) 