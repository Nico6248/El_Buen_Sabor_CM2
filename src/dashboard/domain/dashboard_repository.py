from abc import ABC, abstractmethod
from typing import List
from datetime import date, datetime
from .dashboard_model import (
    ReservationStats, PopularDishStats, TimeSlotStats, 
    RestaurantStats, DashboardStats
)

class DashboardRepository(ABC):
    """Repositorio abstracto para estadísticas del dashboard"""
    
    @abstractmethod
    def get_reservation_stats(self, start_date: date = None, end_date: date = None) -> ReservationStats:
        """Obtiene estadísticas de reservas"""
        pass
    
    @abstractmethod
    def get_popular_dishes(self, limit: int = 5) -> List[PopularDishStats]:
        """Obtiene los platos más populares basado en preórdenes"""
        pass
    
    @abstractmethod
    def get_popular_time_slots(self, limit: int = 5) -> List[TimeSlotStats]:
        """Obtiene los horarios más populares para reservas"""
        pass
    
    @abstractmethod
    def get_restaurant_stats(self) -> List[RestaurantStats]:
        """Obtiene estadísticas por restaurante"""
        pass
    
    @abstractmethod
    def get_dashboard_stats(self) -> DashboardStats:
        """Obtiene todas las estadísticas del dashboard"""
        pass 