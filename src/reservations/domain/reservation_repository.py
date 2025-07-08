from abc import ABC, abstractmethod
from typing import List, Optional
from .reservation_model import Reservation, ReservationCreate

class IReservationRepository(ABC):
    @abstractmethod
    def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        pass

    @abstractmethod
    def get_by_user(self, user_id: int) -> List[Reservation]:
        pass

    @abstractmethod
    def get_all(self) -> List[Reservation]:
        pass

    @abstractmethod
    def create(self, reservation: ReservationCreate) -> Reservation:
        pass

    @abstractmethod
    def cancel(self, reservation_id: int) -> None:
        pass 