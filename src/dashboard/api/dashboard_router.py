# src/dashboard/api/dashboard_router.py
from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from src.shared.database import get_session

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def get_dashboard_stats(session: Session = Depends(get_session)):
    """Endpoint temporal para estadísticas del dashboard"""
    return {"message": "Dashboard funcionando"}

@router.get("/reservations", status_code=status.HTTP_200_OK)
def get_reservation_stats(session: Session = Depends(get_session)):
    """Endpoint temporal para estadísticas de reservas"""
    return {"message": "Estadísticas de reservas funcionando"} 