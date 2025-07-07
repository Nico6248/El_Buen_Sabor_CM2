# src/main.py
from fastapi import FastAPI
from src.shared.database import create_db_and_tables
from src.auth.api.auth_router import router as auth_router
from src.restaurants.api.restaurant_router import router as restaurant_router
from src.menu.api.menu_router import router as menu_router
from src.reservations.api.reservation_router import router as reservation_router
from src.dashboard.api.dashboard_router import router as dashboard_router
from src.shared.exceptions import setup_exception_handlers

# Creación de la instancia de FastAPI
app = FastAPI(
    title="El Buen Sabor API",
    description="API para la gestión de reservas de restaurantes 'El Buen Sabor'",
    version="1.0.0",
)

# Configuración de manejadores de excepciones personalizados
setup_exception_handlers(app)

# Hook para crear tablas al iniciar (opcional, Alembic es preferido)
@app.on_event("startup")
def on_startup():
    # En un entorno de producción, las migraciones con Alembic son la mejor práctica.
    # Esta función es útil para desarrollo y pruebas rápidas.
    # create_db_and_tables()
    pass

# Inclusión de los routers de los diferentes módulos
app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
app.include_router(restaurant_router, prefix="/restaurants", tags=["Restaurantes"])
app.include_router(menu_router, prefix="/menu", tags=["Menú"])
app.include_router(reservation_router, prefix="/reservations", tags=["Reservas"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])


@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raíz para verificar que la API está funcionando.
    """
    return {"message": "Bienvenido a la API de El Buen Sabor"}

