from typing import List
from datetime import date, datetime, timedelta
from sqlmodel import Session, select, func
from sqlalchemy import and_, extract, case, text

from src.dashboard.domain.dashboard_repository import DashboardRepository
from src.dashboard.domain.dashboard_model import (
    ReservationStats, PopularDishStats, TimeSlotStats, 
    RestaurantStats, DashboardStats
)
from src.reservations.domain.reservation_model import Reservation
from src.restaurants.domain.restaurant_model import Restaurant, Table
from src.menu.domain.menu_model import Dish

class DashboardRepositoryDB(DashboardRepository):
    """Implementación del repositorio de dashboard usando PostgreSQL"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_reservation_stats(self, start_date: date = None, end_date: date = None) -> ReservationStats:
        """Obtiene estadísticas de reservas"""
        # Construir filtros de fecha
        filters = []
        if start_date:
            filters.append(Reservation.date >= start_date)
        if end_date:
            filters.append(Reservation.date <= end_date)
        
        # Estadísticas generales
        total_query = select(func.count(Reservation.id))
        if filters:
            total_query = total_query.where(and_(*filters))
        total_reservations = self.session.exec(total_query).first() or 0
        
        # Estadísticas por estado
        confirmed_query = select(func.count(Reservation.id)).where(Reservation.status == "confirmed")
        if filters:
            confirmed_query = confirmed_query.where(and_(*filters))
        confirmed_reservations = self.session.exec(confirmed_query).first() or 0
        
        pending_query = select(func.count(Reservation.id)).where(Reservation.status == "pending")
        if filters:
            pending_query = pending_query.where(and_(*filters))
        pending_reservations = self.session.exec(pending_query).first() or 0
        
        cancelled_query = select(func.count(Reservation.id)).where(Reservation.status == "cancelled")
        if filters:
            cancelled_query = cancelled_query.where(and_(*filters))
        cancelled_reservations = self.session.exec(cancelled_query).first() or 0
        
        # Estadísticas por período
        today = date.today()
        today_reservations = self.session.exec(
            select(func.count(Reservation.id)).where(Reservation.date == today)
        ).first() or 0
        
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        this_week_reservations = self.session.exec(
            select(func.count(Reservation.id)).where(
                and_(Reservation.date >= week_start, Reservation.date <= week_end)
            )
        ).first() or 0
        
        month_start = today.replace(day=1)
        if today.month == 12:
            month_end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
        this_month_reservations = self.session.exec(
            select(func.count(Reservation.id)).where(
                and_(Reservation.date >= month_start, Reservation.date <= month_end)
            )
        ).first() or 0
        
        return ReservationStats(
            total_reservations=total_reservations,
            confirmed_reservations=confirmed_reservations,
            pending_reservations=pending_reservations,
            cancelled_reservations=cancelled_reservations,
            today_reservations=today_reservations,
            this_week_reservations=this_week_reservations,
            this_month_reservations=this_month_reservations
        )
    
    def get_popular_dishes(self, limit: int = 5) -> List[PopularDishStats]:
        """Obtiene los platos más populares basado en preórdenes"""
        # Por ahora, como no tenemos un sistema complejo de preórdenes,
        # simulamos estadísticas basadas en platos existentes
        dishes = self.session.exec(select(Dish).limit(limit)).all()
        
        popular_dishes = []
        for i, dish in enumerate(dishes):
            # Simular estadísticas (en un sistema real, esto vendría de análisis de preórdenes)
            reservation_count = (i + 1) * 3  # Simulación
            total_orders = reservation_count * 2  # Simulación
            
            popular_dishes.append(PopularDishStats(
                dish_id=dish.id,
                dish_name=dish.name,
                reservation_count=reservation_count,
                total_orders=total_orders
            ))
        
        return popular_dishes
    
    def get_popular_time_slots(self, limit: int = 5) -> List[TimeSlotStats]:
        """Obtiene los horarios más populares para reservas"""
        # Agrupar reservas por hora de inicio
        time_slots_query = select(
            func.extract('hour', Reservation.start_time).label('hour'),
            func.count(Reservation.id).label('count')
        ).group_by(text('hour')).order_by(text('count DESC')).limit(limit)
        
        time_slots = self.session.exec(time_slots_query).all()
        
        # Calcular total para porcentajes
        total_reservations = self.session.exec(select(func.count(Reservation.id))).first() or 1
        
        popular_time_slots = []
        for hour, count in time_slots:
            percentage = (count / total_reservations) * 100
            popular_time_slots.append(TimeSlotStats(
                time_slot=f"{int(hour):02d}:00",
                reservation_count=count,
                percentage=round(percentage, 2)
            ))
        
        return popular_time_slots
    
    def get_restaurant_stats(self) -> List[RestaurantStats]:
        """Obtiene estadísticas por restaurante"""
        restaurants = self.session.exec(select(Restaurant)).all()
        
        restaurant_stats = []
        for restaurant in restaurants:
            # Contar reservas por restaurante
            reservation_count = self.session.exec(
                select(func.count(Reservation.id)).where(Reservation.restaurant_id == restaurant.id)
            ).first() or 0
            
            # Calcular capacidad promedio de las mesas
            tables = self.session.exec(
                select(Table).where(Table.restaurant_id == restaurant.id)
            ).all()
            
            if tables:
                average_capacity = sum(table.capacity for table in tables) / len(tables)
            else:
                average_capacity = 0
            
            # Encontrar horario más popular
            popular_time = self.session.exec(
                select(
                    func.extract('hour', Reservation.start_time).label('hour'),
                    func.count(Reservation.id).label('count')
                ).where(Reservation.restaurant_id == restaurant.id)
                .group_by(text('hour'))
                .order_by(text('count DESC'))
                .limit(1)
            ).first()
            
            most_popular_time = f"{int(popular_time[0]):02d}:00" if popular_time else "N/A"
            
            restaurant_stats.append(RestaurantStats(
                restaurant_id=restaurant.id,
                restaurant_name=restaurant.name,
                total_reservations=reservation_count,
                average_capacity=round(average_capacity, 2),
                most_popular_time=most_popular_time
            ))
        
        return restaurant_stats
    
    def get_dashboard_stats(self) -> DashboardStats:
        """Obtiene todas las estadísticas del dashboard"""
        return DashboardStats(
            reservation_stats=self.get_reservation_stats(),
            popular_dishes=self.get_popular_dishes(),
            popular_time_slots=self.get_popular_time_slots(),
            restaurant_stats=self.get_restaurant_stats(),
            last_updated=datetime.now()
        ) 