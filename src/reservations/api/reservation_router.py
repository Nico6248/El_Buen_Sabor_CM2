# src/reservations/api/reservation_router.py
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import datetime, time, date as date_cls

from src.shared.database import get_session
from src.reservations.domain.reservation_model import Reservation, ReservationCreate, ReservationRead
from src.auth.infrastructure.security_service import get_current_user
from src.auth.domain.user_model import User, UserRole
from src.restaurants.domain.restaurant_model import Restaurant
from src.reservations.infrastructure.reservation_repository_db import ReservationRepositoryDB

router = APIRouter()

@router.get("/", response_model=List[ReservationRead], status_code=status.HTTP_200_OK)
def get_reservations(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    repo = ReservationRepositoryDB(session)
    if current_user.role == UserRole.ADMIN:
        reservas = repo.get_all()
    else:
        reservas = repo.get_by_user(current_user.id)
    return reservas

@router.post("/", response_model=ReservationRead, status_code=status.HTTP_201_CREATED)
def create_reservation(reservation_in: ReservationCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    # Validar que la reserva es para el usuario autenticado
    if current_user.role != UserRole.ADMIN and reservation_in.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes crear reservas para otros usuarios.")
    # Validar límite de platos preordenados
    if reservation_in.preordered_dishes:
        ids = [x for x in reservation_in.preordered_dishes.split(",") if x.strip()]
        if len(ids) > 5:
            raise HTTPException(status_code=400, detail="No puedes preordenar más de 5 platos por reserva.")
    # Validar que la reserva esté dentro del horario del restaurante
    restaurante = session.get(Restaurant, reservation_in.restaurant_id)
    if not restaurante:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado.")
    opening = restaurante.opening_time.replace(tzinfo=None) if restaurante.opening_time.tzinfo else restaurante.opening_time
    closing = restaurante.closing_time.replace(tzinfo=None) if restaurante.closing_time.tzinfo else restaurante.closing_time
    start = reservation_in.start_time.replace(tzinfo=None) if reservation_in.start_time.tzinfo else reservation_in.start_time
    end = reservation_in.end_time.replace(tzinfo=None) if reservation_in.end_time.tzinfo else reservation_in.end_time
    if not (opening <= start < closing and opening < end <= closing):
        raise HTTPException(status_code=400, detail="La reserva debe estar dentro del horario de apertura y cierre del restaurante.")
    # No permitir reservas en el pasado
    now = datetime.now()
    reserva_datetime = datetime.combine(reservation_in.date, start)
    if reserva_datetime < now:
        raise HTTPException(status_code=400, detail="No puedes reservar en el pasado.")
    # Validar solapamiento de horarios en la misma mesa
    reservas_existentes = session.exec(
        select(Reservation).where(
            Reservation.table_id == reservation_in.table_id,
            Reservation.date == reservation_in.date,
            Reservation.status != "cancelled"
        )
    ).all()
    for r in reservas_existentes:
        # Asegurar que todos los tiempos tengan el mismo formato (sin zona horaria)
        r_start = r.start_time.replace(tzinfo=None) if r.start_time.tzinfo else r.start_time
        r_end = r.end_time.replace(tzinfo=None) if r.end_time.tzinfo else r.end_time
        new_start = reservation_in.start_time.replace(tzinfo=None) if reservation_in.start_time.tzinfo else reservation_in.start_time
        new_end = reservation_in.end_time.replace(tzinfo=None) if reservation_in.end_time.tzinfo else reservation_in.end_time
        
        if not (new_end <= r_start or new_start >= r_end):
            raise HTTPException(status_code=409, detail="La mesa ya está reservada en ese horario.")
    # Crear reserva
    repo = ReservationRepositoryDB(session)
    reserva = repo.create(reservation_in)
    return reserva

@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_reservation(reservation_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    repo = ReservationRepositoryDB(session)
    reserva = repo.get_by_id(reservation_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    # Solo el dueño o admin puede cancelar
    if current_user.role != UserRole.ADMIN and reserva.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para cancelar esta reserva")
    if reserva.status == "cancelled":
        raise HTTPException(status_code=400, detail="La reserva ya está cancelada")
    repo.cancel(reservation_id)
    return 