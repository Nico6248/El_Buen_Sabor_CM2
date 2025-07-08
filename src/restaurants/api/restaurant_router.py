# src/restaurants/api/restaurant_router.py
from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from typing import List

from src.shared.database import get_session
from src.restaurants.domain.restaurant_model import (
    Restaurant, RestaurantCreate, RestaurantRead,
    Table, TableCreate, TableRead
)
from src.shared.exceptions import BusinessException
from src.auth.infrastructure.security_service import get_current_user, admin_required

router = APIRouter()

# Endpoints para Restaurantes
@router.post("/", response_model=RestaurantRead, status_code=status.HTTP_201_CREATED)
def create_restaurant(restaurant: RestaurantCreate, session: Session = Depends(get_session), current_user=Depends(admin_required)):
    # Solo admin puede crear restaurantes
    if restaurant.closing_time <= restaurant.opening_time:
        raise BusinessException(detail="La hora de cierre debe ser posterior a la de apertura.")
    
    db_restaurant = Restaurant.from_orm(restaurant)
    session.add(db_restaurant)
    session.commit()
    session.refresh(db_restaurant)
    return db_restaurant

@router.get("/", response_model=List[RestaurantRead])
def get_all_restaurants(session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    restaurants = session.exec(select(Restaurant)).all()
    return restaurants

# Endpoints para Mesas
@router.post("/tables", response_model=TableRead, status_code=status.HTTP_201_CREATED)
def create_table(table: TableCreate, session: Session = Depends(get_session), current_user=Depends(admin_required)):
    # Solo admin puede crear mesas
    restaurant = session.get(Restaurant, table.restaurant_id)
    if not restaurant:
        raise BusinessException(status_code=404, detail="Restaurante no encontrado.")
    
    # Validar que el número de mesa no se repita en el mismo restaurante
    existing_table = session.exec(
        select(Table).where(Table.restaurant_id == table.restaurant_id, Table.table_number == table.table_number)
    ).first()
    if existing_table:
        raise BusinessException(status_code=409, detail="El número de mesa ya existe en este restaurante.")

    db_table = Table.from_orm(table)
    session.add(db_table)
    session.commit()
    session.refresh(db_table)
    return db_table

@router.get("/{restaurant_id}/tables", response_model=List[TableRead])
def get_tables_for_restaurant(restaurant_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    tables = session.exec(select(Table).where(Table.restaurant_id == restaurant_id)).all()
    if not tables:
         raise BusinessException(status_code=404, detail="No se encontraron mesas para este restaurante o el restaurante no existe.")
    return tables
