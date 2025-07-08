# src/dashboard/api/dashboard_router.py
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from typing import List
from datetime import date

from src.shared.database import get_session
from src.auth.infrastructure.security_service import admin_required
from src.auth.domain.user_model import User
from src.dashboard.domain.dashboard_service import DashboardService
from src.dashboard.infrastructure.dashboard_repository_db import DashboardRepositoryDB
from src.dashboard.domain.dashboard_model import (
    ReservationStats, PopularDishStats, TimeSlotStats, 
    RestaurantStats, DashboardStats
)

router = APIRouter()

def get_dashboard_service(session: Session = Depends(get_session)) -> DashboardService:
    """Dependency injection para el servicio de dashboard"""
    repository = DashboardRepositoryDB(session)
    return DashboardService(repository)

@router.get("/", response_model=DashboardStats, status_code=status.HTTP_200_OK)
def get_dashboard_stats(
    service: DashboardService = Depends(get_dashboard_service),
    current_user: User = Depends(admin_required)
):
    """Obtiene todas las estadísticas del dashboard (solo admin)"""
    try:
        return service.get_dashboard_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

@router.get("/reservations", response_model=ReservationStats, status_code=status.HTTP_200_OK)
def get_reservation_stats(
    start_date: date = None,
    end_date: date = None,
    service: DashboardService = Depends(get_dashboard_service),
    current_user: User = Depends(admin_required)
):
    """Obtiene estadísticas de reservas con filtros opcionales (solo admin)"""
    try:
        return service.get_reservation_stats(start_date, end_date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

@router.get("/popular-dishes", response_model=List[PopularDishStats], status_code=status.HTTP_200_OK)
def get_popular_dishes(
    limit: int = 5,
    service: DashboardService = Depends(get_dashboard_service),
    current_user: User = Depends(admin_required)
):
    """Obtiene los platos más populares (solo admin)"""
    try:
        return service.get_popular_dishes(limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener platos populares: {str(e)}")

@router.get("/popular-time-slots", response_model=List[TimeSlotStats], status_code=status.HTTP_200_OK)
def get_popular_time_slots(
    limit: int = 5,
    service: DashboardService = Depends(get_dashboard_service),
    current_user: User = Depends(admin_required)
):
    """Obtiene los horarios más populares (solo admin)"""
    try:
        return service.get_popular_time_slots(limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener horarios populares: {str(e)}")

@router.get("/restaurants", response_model=List[RestaurantStats], status_code=status.HTTP_200_OK)
def get_restaurant_stats(
    service: DashboardService = Depends(get_dashboard_service),
    current_user: User = Depends(admin_required)
):
    """Obtiene estadísticas por restaurante (solo admin)"""
    try:
        return service.get_restaurant_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas de restaurantes: {str(e)}") 