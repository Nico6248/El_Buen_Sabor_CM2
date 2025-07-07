# src/auth/domain/user_model.py
from typing import Optional
from sqlmodel import Field, SQLModel

class UserRole:
    CLIENT = "client"
    ADMIN = "admin"

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    full_name: str
    role: str = Field(default=UserRole.CLIENT)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

# ---

