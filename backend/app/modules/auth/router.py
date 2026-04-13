# =============================================================================
# modules/auth/router.py — Endpoints de autenticación
# =============================================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.schema import LoginRequest, TokenResponse
from app.modules.auth.service import auth_service
from app.modules.usuario.schema import UsuarioResponse
from app.core.dependencies import get_current_user
from app.modules.usuario.model import Usuario

router = APIRouter()


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión",
    description="Recibe email y contraseña. Si son correctos retorna un token JWT."
)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint de login.

    El frontend debe guardar el token retornado y enviarlo en cada
    petición protegida en el header:
        Authorization: Bearer <access_token>
    """
    return auth_service.login(db, datos)


@router.get(
    "/me",
    response_model=UsuarioResponse,
    summary="Obtener usuario autenticado",
    description="Retorna los datos del usuario dueño del token JWT enviado."
)
def obtener_usuario_actual(
    current_user: Usuario = Depends(get_current_user)
):
    """
    Endpoint útil para que el frontend sepa qué usuario está logueado
    y qué rol tiene, sin necesitar otra llamada a /usuarios.
    """
    return current_user