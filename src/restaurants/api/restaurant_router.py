# src/restaurants/api/restaurant_router.py
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from typing import List

from src.shared.database import get_session
from src.restaurants.domain.restaurant_model import (
    Restaurant, RestaurantCreate, RestaurantRead,
    Table, TableCreate, TableRead
)
from src.shared.exceptions import BusinessException
from src.auth.infrastructure.security_service import get_current_user, admin_required
from src.restaurants.domain.restaurant_service import RestaurantService
from src.restaurants.infrastructure.restaurant_repository_db import RestaurantRepositoryDB

router = APIRouter()

def get_restaurant_service(session: Session = Depends(get_session)) -> RestaurantService:
    """Dependency injection para el servicio de restaurantes"""
    repository = RestaurantRepositoryDB(session)
    return RestaurantService(repository)

# Endpoints para Restaurantes
@router.post("/", response_model=RestaurantRead, status_code=status.HTTP_201_CREATED)
def create_restaurant(
    restaurant: RestaurantCreate, 
    session: Session = Depends(get_session), 
    current_user=Depends(admin_required)
):
    """Crea un nuevo restaurante (solo admin)"""
    try:
        service = get_restaurant_service(session)
        return service.create_restaurant(restaurant)
    except ValueError as e:
        raise BusinessException(detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear restaurante: {str(e)}")

@router.get("/", response_model=List[RestaurantRead])
def get_all_restaurants(
    session: Session = Depends(get_session), 
    current_user=Depends(get_current_user)
):
    """Obtiene todos los restaurantes (usuarios autenticados)"""
    try:
        service = get_restaurant_service(session)
        return service.get_all_restaurants()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener restaurantes: {str(e)}")

@router.get("/{restaurant_id}", response_model=RestaurantRead)
def get_restaurant_by_id(
    restaurant_id: int, 
    session: Session = Depends(get_session), 
    current_user=Depends(get_current_user)
):
    """Obtiene un restaurante específico por ID (usuarios autenticados)"""
    try:
        service = get_restaurant_service(session)
        restaurant = service.get_restaurant_by_id(restaurant_id)
        if not restaurant:
            raise BusinessException(status_code=404, detail="Restaurante no encontrado")
        return restaurant
    except BusinessException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener restaurante: {str(e)}")

@router.put("/{restaurant_id}", response_model=RestaurantRead)
def update_restaurant(
    restaurant_id: int, 
    restaurant: RestaurantCreate, 
    session: Session = Depends(get_session), 
    current_user=Depends(admin_required)
):
    """Actualiza un restaurante (solo admin)"""
    try:
        service = get_restaurant_service(session)
        updated_restaurant = service.update_restaurant(restaurant_id, restaurant)
        if not updated_restaurant:
            raise BusinessException(status_code=404, detail="Restaurante no encontrado")
        return updated_restaurant
    except ValueError as e:
        raise BusinessException(detail=str(e))
    except BusinessException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar restaurante: {str(e)}")

@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(
    restaurant_id: int, 
    session: Session = Depends(get_session), 
    current_user=Depends(admin_required)
):
    """Elimina un restaurante (solo admin)"""
    try:
        service = get_restaurant_service(session)
        success = service.delete_restaurant(restaurant_id)
        if not success:
            raise BusinessException(status_code=404, detail="Restaurante no encontrado")
    except ValueError as e:
        raise BusinessException(detail=str(e))
    except BusinessException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar restaurante: {str(e)}")

# Endpoints para Mesas
@router.post("/tables", response_model=TableRead, status_code=status.HTTP_201_CREATED)
def create_table(
    table: TableCreate, 
    session: Session = Depends(get_session), 
    current_user=Depends(admin_required)
):
    """Crea una nueva mesa (solo admin)"""
    try:
        service = get_restaurant_service(session)
        return service.create_table(table)
    except ValueError as e:
        raise BusinessException(detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear mesa: {str(e)}")

@router.get("/tables/{table_id}", response_model=TableRead)
def get_table_by_id(
    table_id: int, 
    session: Session = Depends(get_session), 
    current_user=Depends(get_current_user)
):
    """Obtiene una mesa específica por ID (usuarios autenticados)"""
    try:
        service = get_restaurant_service(session)
        table = service.get_table_by_id(table_id)
        if not table:
            raise BusinessException(status_code=404, detail="Mesa no encontrada")
        return table
    except BusinessException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener mesa: {str(e)}")

@router.get("/{restaurant_id}/tables", response_model=List[TableRead])
def get_tables_for_restaurant(
    restaurant_id: int, 
    session: Session = Depends(get_session), 
    current_user=Depends(get_current_user)
):
    """Obtiene todas las mesas de un restaurante (usuarios autenticados)"""
    try:
        service = get_restaurant_service(session)
        return service.get_tables_by_restaurant(restaurant_id)
    except ValueError as e:
        raise BusinessException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener mesas: {str(e)}")

@router.put("/tables/{table_id}", response_model=TableRead)
def update_table(
    table_id: int, 
    table: TableCreate, 
    session: Session = Depends(get_session), 
    current_user=Depends(admin_required)
):
    """Actualiza una mesa (solo admin)"""
    try:
        service = get_restaurant_service(session)
        updated_table = service.update_table(table_id, table)
        if not updated_table:
            raise BusinessException(status_code=404, detail="Mesa no encontrada")
        return updated_table
    except ValueError as e:
        raise BusinessException(detail=str(e))
    except BusinessException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar mesa: {str(e)}")

@router.delete("/tables/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(
    table_id: int, 
    session: Session = Depends(get_session), 
    current_user=Depends(admin_required)
):
    """Elimina una mesa (solo admin)"""
    try:
        service = get_restaurant_service(session)
        success = service.delete_table(table_id)
        if not success:
            raise BusinessException(status_code=404, detail="Mesa no encontrada")
    except ValueError as e:
        raise BusinessException(detail=str(e))
    except BusinessException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar mesa: {str(e)}")
