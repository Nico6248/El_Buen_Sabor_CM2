# src/menu/api/menu_router.py
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from typing import List

from src.shared.database import get_session
from src.menu.domain.menu_model import Dish, DishCreate, DishRead, DishCategory
from src.shared.exceptions import BusinessException
from src.restaurants.domain.restaurant_model import Restaurant
from src.auth.infrastructure.security_service import get_current_user, admin_required
from src.menu.domain.menu_service import MenuService
from src.menu.infrastructure.menu_repository_db import MenuRepositoryDB

router = APIRouter()

def get_menu_service(session: Session = Depends(get_session)) -> MenuService:
    """Dependency injection para el servicio de menú"""
    repository = MenuRepositoryDB(session)
    return MenuService(repository)

@router.post("/", response_model=DishRead, status_code=status.HTTP_201_CREATED)
def create_dish(
    dish: DishCreate, 
    session: Session = Depends(get_session), 
    current_user=Depends(admin_required)
):
    """Crea un nuevo plato (solo admin)"""
    try:
        # Verificar que el restaurante existe
        restaurant = session.get(Restaurant, dish.restaurant_id)
        restaurant_exists = restaurant is not None
        
        service = get_menu_service(session)
        return service.create_dish(dish, restaurant_exists)
    except ValueError as e:
        raise BusinessException(detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear plato: {str(e)}")

@router.get("/restaurant/{restaurant_id}", response_model=List[DishRead])
def get_menu_for_restaurant(
    restaurant_id: int, 
    session: Session = Depends(get_session), 
    current_user=Depends(get_current_user)
):
    """Obtiene el menú de un restaurante (usuarios autenticados)"""
    try:
        service = get_menu_service(session)
        return service.get_menu_for_restaurant(restaurant_id)
    except ValueError as e:
        raise BusinessException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener menú: {str(e)}")

@router.get("/", response_model=List[DishRead])
def get_all_dishes(
    session: Session = Depends(get_session), 
    current_user=Depends(admin_required)
):
    """Obtiene todos los platos (solo admin)"""
    try:
        service = get_menu_service(session)
        return service.get_all_dishes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener platos: {str(e)}")

@router.get("/{dish_id}", response_model=DishRead)
def get_dish_by_id(
    dish_id: int, 
    session: Session = Depends(get_session), 
    current_user=Depends(get_current_user)
):
    """Obtiene un plato específico por ID (usuarios autenticados)"""
    try:
        service = get_menu_service(session)
        dish = service.get_dish_by_id(dish_id)
        if not dish:
            raise BusinessException(status_code=404, detail="Plato no encontrado")
        return dish
    except BusinessException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener plato: {str(e)}")

@router.put("/{dish_id}", response_model=DishRead)
def update_dish(
    dish_id: int, 
    dish: DishCreate, 
    session: Session = Depends(get_session), 
    current_user=Depends(admin_required)
):
    """Actualiza un plato (solo admin)"""
    try:
        # Verificar que el restaurante existe
        restaurant = session.get(Restaurant, dish.restaurant_id)
        restaurant_exists = restaurant is not None
        
        service = get_menu_service(session)
        updated_dish = service.update_dish(dish_id, dish, restaurant_exists)
        if not updated_dish:
            raise BusinessException(status_code=404, detail="Plato no encontrado")
        return updated_dish
    except ValueError as e:
        raise BusinessException(detail=str(e))
    except BusinessException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar plato: {str(e)}")

@router.delete("/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dish(
    dish_id: int, 
    session: Session = Depends(get_session), 
    current_user=Depends(admin_required)
):
    """Elimina un plato (solo admin)"""
    try:
        service = get_menu_service(session)
        success = service.delete_dish(dish_id)
        if not success:
            raise BusinessException(status_code=404, detail="Plato no encontrado")
    except ValueError as e:
        raise BusinessException(detail=str(e))
    except BusinessException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar plato: {str(e)}")