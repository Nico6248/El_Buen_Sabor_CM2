from typing import List
from datetime import date, datetime
from .dashboard_repository import DashboardRepository
from .dashboard_model import (
    ReservationStats, PopularDishStats, TimeSlotStats, 
    RestaurantStats, DashboardStats
)

class DashboardService:
    """Servicio de aplicación para el dashboard"""
    
    def __init__(self, repository: DashboardRepository):
        self.repository = repository
    
    def get_reservation_stats(self, start_date: date = None, end_date: date = None) -> ReservationStats:
        """Obtiene estadísticas de reservas con validaciones de negocio"""
        if start_date and end_date and start_date > end_date:
            raise ValueError("La fecha de inicio no puede ser posterior a la fecha de fin")
        
        return self.repository.get_reservation_stats(start_date, end_date)
    
    def get_popular_dishes(self, limit: int = 5) -> List[PopularDishStats]:
        """Obtiene los platos más populares con validación de límite"""
        if limit <= 0 or limit > 20:
            raise ValueError("El límite debe estar entre 1 y 20")
        
        return self.repository.get_popular_dishes(limit)
    
    def get_popular_time_slots(self, limit: int = 5) -> List[TimeSlotStats]:
        """Obtiene los horarios más populares con validación de límite"""
        if limit <= 0 or limit > 24:
            raise ValueError("El límite debe estar entre 1 y 24")
        
        return self.repository.get_popular_time_slots(limit)
    
    def get_restaurant_stats(self) -> List[RestaurantStats]:
        """Obtiene estadísticas por restaurante"""
        return self.repository.get_restaurant_stats()
    
    def get_dashboard_stats(self) -> DashboardStats:
        """Obtiene todas las estadísticas del dashboard"""
        return self.repository.get_dashboard_stats() 