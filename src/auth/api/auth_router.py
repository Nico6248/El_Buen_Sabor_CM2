
# src/auth/api/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from src.shared.database import get_session
from src.auth.domain.user_model import UserCreate, UserRead, UserRole, User
from src.auth.infrastructure import security_service
from src.shared.exceptions import BusinessException

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, session: Session = Depends(get_session)):
    # Asignar rol por defecto si no se proporciona y validar
    user_role = user_in.role or UserRole.CLIENT
    if user_role not in [UserRole.CLIENT, UserRole.ADMIN]:
        raise BusinessException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El rol debe ser 'client' o 'admin'."
        )

    db_user = session.query(User).filter(User.email == user_in.email).first()
    if db_user:
        raise BusinessException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo electrónico ya está registrado."
        )
    
    hashed_password = security_service.get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed_password,
        role=user_role
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == form_data.username).first()
    if not user or not security_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    scopes = [f"{user.role}:read", f"{user.role}:write"]
    access_token = security_service.create_access_token(
        data={"sub": user.email, "scopes": scopes}
    )
    return {"access_token": access_token, "token_type": "bearer"}
