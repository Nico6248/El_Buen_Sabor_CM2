# src/menu/domain/menu_model.py
from typing import Optional
from sqlmodel import Field, SQLModel

class DishCategory:
    ENTRADA = "Entrada"
    PRINCIPAL = "Principal"
    POSTRE = "Postre"
    BEBIDA = "Bebida"

class DishBase(SQLModel):
    name: str
    description: str
    category: str
    restaurant_id: int = Field(foreign_key="restaurant.id")
    is_available: bool = Field(default=True)

class Dish(DishBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class DishCreate(DishBase):
    pass

class DishRead(DishBase):
    id: int