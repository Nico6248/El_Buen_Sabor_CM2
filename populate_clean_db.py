#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos limpios
Todos los IDs empezarán desde 1
"""

import os
import sys
from datetime import time, date, datetime
from sqlmodel import Session, create_engine

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.shared.database import engine
from src.auth.domain.user_model import User, UserRole
from src.auth.infrastructure.security_service import get_password_hash
from src.restaurants.domain.restaurant_model import Restaurant, Table
from src.menu.domain.menu_model import Dish, DishCategory

def create_users(session: Session):
    """Crear usuarios de ejemplo"""
    print("🔄 Creando usuarios...")
    
    users = [
        {
            "email": "admin@admin.com",
            "full_name": "Administrador",
            "password": "admin123",
            "role": UserRole.ADMIN
        },
        {
            "email": "cliente1@email.com",
            "full_name": "Juan Pérez",
            "password": "password123",
            "role": UserRole.CLIENT
        },
        {
            "email": "cliente2@email.com",
            "full_name": "María García",
            "password": "password123",
            "role": UserRole.CLIENT
        },
        {
            "email": "cliente3@email.com",
            "full_name": "Carlos López",
            "password": "password123",
            "role": UserRole.CLIENT
        }
    ]
    
    for user_data in users:
        hashed_password = get_password_hash(user_data["password"])
        user = User(
            email=user_data["email"],
            full_name=user_data["full_name"],
            hashed_password=hashed_password,
            role=user_data["role"]
        )
        session.add(user)
    
    session.commit()
    print("✅ Usuarios creados exitosamente")

def create_restaurants(session: Session):
    """Crear restaurantes de ejemplo"""
    print("🔄 Creando restaurantes...")
    
    restaurants = [
        {
            "name": "El Buen Sabor",
            "location": "Centro de la ciudad",
            "opening_time": time(12, 0),  # 12:00
            "closing_time": time(23, 0)   # 23:00
        },
        {
            "name": "La Terraza",
            "location": "Zona norte",
            "opening_time": time(11, 30),  # 11:30
            "closing_time": time(22, 30)   # 22:30
        }
    ]
    
    for restaurant_data in restaurants:
        restaurant = Restaurant(**restaurant_data)
        session.add(restaurant)
    
    session.commit()
    print("✅ Restaurantes creados exitosamente")

def create_tables(session: Session):
    """Crear mesas de ejemplo"""
    print("🔄 Creando mesas...")
    
    # Obtener restaurantes
    restaurants = session.query(Restaurant).all()
    
    tables_data = [
        # Restaurante 1 (El Buen Sabor)
        {"table_number": 1, "capacity": 4, "location_in_restaurant": "terraza", "restaurant_id": 1},
        {"table_number": 2, "capacity": 6, "location_in_restaurant": "interior", "restaurant_id": 1},
        {"table_number": 3, "capacity": 2, "location_in_restaurant": "terraza", "restaurant_id": 1},
        {"table_number": 4, "capacity": 8, "location_in_restaurant": "interior", "restaurant_id": 1},
        {"table_number": 5, "capacity": 4, "location_in_restaurant": "terraza", "restaurant_id": 1},
        
        # Restaurante 2 (La Terraza)
        {"table_number": 1, "capacity": 6, "location_in_restaurant": "terraza", "restaurant_id": 2},
        {"table_number": 2, "capacity": 4, "location_in_restaurant": "interior", "restaurant_id": 2},
        {"table_number": 3, "capacity": 8, "location_in_restaurant": "terraza", "restaurant_id": 2},
    ]
    
    for table_data in tables_data:
        table = Table(**table_data)
        session.add(table)
    
    session.commit()
    print("✅ Mesas creadas exitosamente")

def create_dishes(session: Session):
    """Crear platos de ejemplo"""
    print("🔄 Creando platos...")
    
    dishes_data = [
        # Restaurante 1 (El Buen Sabor)
        {"name": "Pizza Margherita", "description": "Pizza clásica con tomate y mozzarella", "category": DishCategory.PRINCIPAL, "restaurant_id": 1, "is_available": True},
        {"name": "Pasta Carbonara", "description": "Pasta con salsa cremosa y panceta", "category": DishCategory.PRINCIPAL, "restaurant_id": 1, "is_available": True},
        {"name": "Ensalada César", "description": "Ensalada fresca con aderezo especial", "category": DishCategory.ENTRADA, "restaurant_id": 1, "is_available": True},
        {"name": "Tiramisú", "description": "Postre italiano con café y mascarpone", "category": DishCategory.POSTRE, "restaurant_id": 1, "is_available": True},
        {"name": "Limonada Natural", "description": "Bebida refrescante de limón", "category": DishCategory.BEBIDA, "restaurant_id": 1, "is_available": True},
        
        # Restaurante 2 (La Terraza)
        {"name": "Parrillada Mixta", "description": "Variedad de carnes a la parrilla", "category": DishCategory.PRINCIPAL, "restaurant_id": 2, "is_available": True},
        {"name": "Sopa del Día", "description": "Sopa casera preparada diariamente", "category": DishCategory.ENTRADA, "restaurant_id": 2, "is_available": True},
        {"name": "Flan Casero", "description": "Postre tradicional con caramelo", "category": DishCategory.POSTRE, "restaurant_id": 2, "is_available": True},
        {"name": "Agua Mineral", "description": "Agua mineral con gas", "category": DishCategory.BEBIDA, "restaurant_id": 2, "is_available": True},
    ]
    
    for dish_data in dishes_data:
        dish = Dish(**dish_data)
        session.add(dish)
    
    session.commit()
    print("✅ Platos creados exitosamente")

def main():
    """Función principal para poblar la base de datos"""
    print("🚀 Iniciando población de base de datos...")
    
    try:
        with Session(engine) as session:
            # Crear datos en orden (por las foreign keys)
            create_users(session)
            create_restaurants(session)
            create_tables(session)
            create_dishes(session)
            
        print("\n🎉 ¡Base de datos poblada exitosamente!")
        print("\n📋 Datos creados:")
        print("   👥 Usuarios: 4 (1 admin, 3 clientes)")
        print("   🏪 Restaurantes: 2")
        print("   🪑 Mesas: 8")
        print("   🍽️ Platos: 9")
        print("\n🔑 Credenciales de acceso:")
        print("   Admin: admin@admin.com / admin123")
        print("   Cliente: cliente1@email.com / password123")
        
    except Exception as e:
        print(f"❌ Error al poblar la base de datos: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 