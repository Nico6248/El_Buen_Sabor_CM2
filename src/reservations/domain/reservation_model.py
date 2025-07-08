from typing import Optional, List
from sqlmodel import Field, SQLModel
from datetime import date, time

class ReservationStatus:
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class ReservationBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    restaurant_id: int = Field(foreign_key="restaurant.id")
    table_id: int = Field(foreign_key="table.id")
    date: date
    start_time: time
    end_time: time
    status: str = Field(default=ReservationStatus.PENDING)
    preordered_dishes: Optional[str] = None  # IDs de platos preordenados como string, ej: "1,2,3"

class Reservation(ReservationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ReservationCreate(ReservationBase):
    pass

class ReservationRead(ReservationBase):
    id: int 