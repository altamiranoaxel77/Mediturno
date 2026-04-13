# =============================================================================
# modules/auth/schema.py — Schemas Pydantic para Autenticación
# =============================================================================

from pydantic import BaseModel, Field, EmailStr


class LoginRequest(BaseModel):
    """
    Datos que recibe el endpoint de login.
    El usuario se identifica con email + password.
    Se usa en: POST /api/v1/auth/login
    """
    email:    EmailStr = Field(..., examples=["juan@hospital.com"])
    password: str      = Field(..., min_length=8, examples=["mipassword123"])


class TokenResponse(BaseModel):
    """
    Respuesta del endpoint de login cuando las credenciales son correctas.
    El frontend debe guardar el access_token y enviarlo en el header
    Authorization: Bearer <token> en cada petición protegida.
    """
    access_token: str = Field(..., examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])

    # token_type siempre es "bearer" — es el estándar para JWT en APIs REST
    token_type: str = Field(default="bearer")


class TokenData(BaseModel):
    """
    Datos que se guardan DENTRO del token JWT (payload).
    Al verificar el token, extraemos estos datos para saber
    qué usuario está haciendo la petición y a qué hospital pertenece.

    IMPORTANTE: no guardar datos sensibles en el token —
    el payload es visible para quien tenga el token (solo está firmado, no cifrado).
    """
    # sub (subject) = identificador del usuario — convención estándar de JWT
    sub:         str | None = None   # email del usuario
    id_usuario:  int | None = None
    id_hospital: int | None = None   # necesario para el filtro multi-tenant
    id_rol:      int | None = None   # necesario para control de acceso por rol