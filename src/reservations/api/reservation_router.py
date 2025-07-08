# src/reservations/api/reservation_router.py
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from typing import List

from src.shared.database import get_session

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def get_reservations(session: Session = Depends(get_session)):
    """Endpoint temporal para reservas"""
    return {"message": "Endpoint de reservas funcionando"}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_reservation(session: Session = Depends(get_session)):
    """Endpoint temporal para crear reservas"""
    return {"message": "Creación de reservas funcionando"} 