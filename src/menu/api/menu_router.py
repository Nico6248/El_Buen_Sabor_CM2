
# src/menu/api/menu_router.py
from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from typing import List

from src.shared.database import get_session
from src.menu.domain.menu_model import Dish, DishCreate, DishRead, DishCategory
from src.shared.exceptions import BusinessException
from src.restaurants.domain.restaurant_model import Restaurant

router = APIRouter()

@router.post("/", response_model=DishRead, status_code=status.HTTP_201_CREATED)
def create_dish(dish: DishCreate, session: Session = Depends(get_session)):
    # Validar que la categoría es válida
    valid_categories = [DishCategory.ENTRADA, DishCategory.PRINCIPAL, DishCategory.POSTRE, DishCategory.BEBIDA]
    if dish.category not in valid_categories:
        raise BusinessException(detail=f"Categoría inválida. Use una de: {valid_categories}")

    # Validar que el restaurante existe
    restaurant = session.get(Restaurant, dish.restaurant_id)
    if not restaurant:
        raise BusinessException(status_code=404, detail="Restaurante no encontrado.")

    # Validar que el nombre del plato es único en el restaurante
    existing_dish = session.exec(
        select(Dish).where(Dish.restaurant_id == dish.restaurant_id, Dish.name == dish.name)
    ).first()
    if existing_dish:
        raise BusinessException(status_code=409, detail="Ya existe un plato con este nombre en el restaurante.")
    
    db_dish = Dish.from_orm(dish)
    session.add(db_dish)
    session.commit()
    session.refresh(db_dish)
    return db_dish

@router.get("/restaurant/{restaurant_id}", response_model=List[DishRead])
def get_menu_for_restaurant(restaurant_id: int, session: Session = Depends(get_session)):
    dishes = session.exec(select(Dish).where(Dish.restaurant_id == restaurant_id, Dish.is_available == True)).all()
    if not dishes:
        raise BusinessException(status_code=404, detail="No se encontró menú para este restaurante.")
    return dishes