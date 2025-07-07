# src/shared/exceptions.py
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

class BusinessException(Exception):
    """Excepción base para errores de lógica de negocio."""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.status_code = status_code
        super().__init__(self.detail)

async def business_exception_handler(request: Request, exc: BusinessException):
    """Manejador para las excepciones de negocio."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

def setup_exception_handlers(app: FastAPI):
    """Añade los manejadores de excepciones a la aplicación FastAPI."""
    app.add_exception_handler(BusinessException, business_exception_handler)

