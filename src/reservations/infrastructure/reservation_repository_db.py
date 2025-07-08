from typing import List, Optional
from sqlmodel import Session, select
from src.reservations.domain.reservation_model import Reservation, ReservationCreate
from src.reservations.domain.reservation_repository import IReservationRepository

class ReservationRepositoryDB(IReservationRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        return self.session.get(Reservation, reservation_id)

    def get_by_user(self, user_id: int) -> List[Reservation]:
        return self.session.exec(select(Reservation).where(Reservation.user_id == user_id)).all()

    def get_all(self) -> List[Reservation]:
        return self.session.exec(select(Reservation)).all()

    def create(self, reservation: ReservationCreate) -> Reservation:
        reserva = Reservation.from_orm(reservation)
        self.session.add(reserva)
        self.session.commit()
        self.session.refresh(reserva)
        return reserva

    def cancel(self, reservation_id: int) -> None:
        reserva = self.session.get(Reservation, reservation_id)
        if reserva:
            reserva.status = "cancelled"
            self.session.add(reserva)
            self.session.commit() 