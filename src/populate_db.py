from src.shared.database import engine
from src.auth.domain.user_model import User, UserRole
from src.restaurants.domain.restaurant_model import Restaurant, Table
from src.menu.domain.menu_model import Dish, DishCategory
from sqlmodel import Session, select
from passlib.context import CryptContext

def populate():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    with Session(engine) as session:
        # Borrar datos previos correctamente
        session.query(Dish).delete()
        session.query(Table).delete()
        session.query(Restaurant).delete()
        session.query(User).delete()
        session.commit()

        # Crear un admin
        admin = User(
            email="admin@admin.com",
            full_name="Administrador",
            hashed_password=pwd_context.hash("admin123"),
            role=UserRole.ADMIN
        )
        session.add(admin)

        # Crear un cliente
        client = User(
            email="cliente@cliente.com",
            full_name="Cliente Ejemplo",
            hashed_password=pwd_context.hash("cliente123"),
            role=UserRole.CLIENT
        )
        session.add(client)

        # Crear un restaurante
        rest = Restaurant(
            name="El Buen Sabor Central",
            location="Calle Falsa 123",
            opening_time="09:00",
            closing_time="23:00"
        )
        session.add(rest)
        session.commit()
        session.refresh(rest)

        # Crear una mesa
        mesa = Table(
            restaurant_id=rest.id,
            table_number=1,
            capacity=4,  # Usa el campo correcto según tu modelo
            location_in_restaurant="Cerca de la ventana"
        )
        session.add(mesa)

        # Crear platos
        plato1 = Dish(
            restaurant_id=rest.id,
            name="Milanesa con papas",
            description="Clásica milanesa argentina con papas fritas",
            price=2500,
            category=DishCategory.PRINCIPAL,
            is_available=True
        )
        plato2 = Dish(
            restaurant_id=rest.id,
            name="Ensalada César",
            description="Ensalada fresca con pollo y aderezo César",
            price=1800,
            category=DishCategory.ENTRADA,
            is_available=True
        )
        plato3 = Dish(
            restaurant_id=rest.id,
            name="Flan casero",
            description="Flan de la casa con dulce de leche",
            price=900,
            category=DishCategory.POSTRE,
            is_available=True
        )
        plato4 = Dish(
            restaurant_id=rest.id,
            name="Agua mineral",
            description="Botella de agua mineral 500ml",
            price=500,
            category=DishCategory.BEBIDA,
            is_available=True
        )
        session.add_all([plato1, plato2, plato3, plato4])

        session.commit()
        print("¡Datos de ejemplo insertados!")

if __name__ == "__main__":
    populate() 