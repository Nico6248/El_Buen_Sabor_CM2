from typing import List, Optional
from sqlmodel import SQLModel
from datetime import date, datetime

class ReservationStats(SQLModel):
    total_reservations: int
    confirmed_reservations: int
    pending_reservations: int
    cancelled_reservations: int
    today_reservations: int
    this_week_reservations: int
    this_month_reservations: int

class PopularDishStats(SQLModel):
    dish_id: int
    dish_name: str
    reservation_count: int
    total_orders: int

class TimeSlotStats(SQLModel):
    time_slot: str
    reservation_count: int
    percentage: float

class RestaurantStats(SQLModel):
    restaurant_id: int
    restaurant_name: str
    total_reservations: int
    average_capacity: float
    most_popular_time: str

class DashboardStats(SQLModel):
    reservation_stats: ReservationStats
    popular_dishes: List[PopularDishStats]
    popular_time_slots: List[TimeSlotStats]
    restaurant_stats: List[RestaurantStats]
    last_updated: datetime 