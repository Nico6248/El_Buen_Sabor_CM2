from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from typing import List

from src.shared.database import get_session
from src.auth.domain.user_model import User, UserRead, UserRole
from src.auth.infrastructure.security_service import admin_required
from src.shared.exceptions import BusinessException

router = APIRouter()

@router.get("/", response_model=List[UserRead], status_code=status.HTTP_200_OK)
def get_all_users(
    session: Session = Depends(get_session), 
    current_user: User = Depends(admin_required)
):
    """Obtiene todos los usuarios (solo admin)"""
    try:
        users = session.exec(select(User)).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def get_user_by_id(
    user_id: int, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(admin_required)
):
    """Obtiene un usuario específico por ID (solo admin)"""
    try:
        user = session.get(User, user_id)
        if not user:
            raise BusinessException(status_code=404, detail="Usuario no encontrado")
        return user
    except BusinessException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuario: {str(e)}") 