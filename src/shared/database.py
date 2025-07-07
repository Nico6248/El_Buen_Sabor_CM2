# src/shared/database.py
import os
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator

# Carga la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/mydatabase")

# Crea el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """
    Crea todas las tablas definidas por los modelos de SQLModel.
    Nota: En producción, es preferible usar Alembic para gestionar las migraciones.
    """
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """
    Generador de dependencias de FastAPI para obtener una sesión de base de datos.
    Asegura que la sesión se cierre después de que la solicitud se complete.
    """
    with Session(engine) as session:
        yield session