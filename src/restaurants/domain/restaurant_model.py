# src/restaurants/domain/restaurant_model.py
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
import datetime

class RestaurantBase(SQLModel):
    name: str = Field(index=True)
    location: str
    opening_time: datetime.time
    closing_time: datetime.time

class Restaurant(RestaurantBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tables: List["Table"] = Relationship(back_populates="restaurant")

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantRead(RestaurantBase):
    id: int

class TableBase(SQLModel):
    table_number: int
    capacity: int = Field(ge=2, le=12)
    location_in_restaurant: str # e.g., "terraza", "interior"

class Table(TableBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant_id: int = Field(foreign_key="restaurant.id")
    restaurant: Restaurant = Relationship(back_populates="tables")

class TableCreate(TableBase):
    restaurant_id: int

class TableRead(TableBase):
    id: int
    restaurant_id: int

# ---