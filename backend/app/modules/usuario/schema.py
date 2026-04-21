# =============================================================================
# modules/usuario/schema.py — Schemas Pydantic para Usuario
# =============================================================================
# REGLA DE ORO: la contraseña entra en UsuarioCreate pero NUNCA
# sale en UsuarioResponse.
#
# id_hospital es opcional (None) solo para el SuperAdmin (id_rol=1).
# Cualquier otro rol debe tener id_hospital.
# =============================================================================

from pydantic import BaseModel, Field, EmailStr


class UsuarioBase(BaseModel):
    """Campos compartidos entre Create y Response (sin password)."""
    nombre:   str      = Field(..., min_length=2, max_length=100, examples=["Juan"])
    apellido: str      = Field(..., min_length=2, max_length=100, examples=["García"])
    dni:      str      = Field(..., min_length=7, max_length=20,  examples=["30123456"])
    email:    EmailStr = Field(...,                                examples=["juan@hospital.com"])


class UsuarioCreate(UsuarioBase):
    """
    Datos para crear un usuario.
    Incluye password — es el ÚNICO schema donde existe este campo.

    id_hospital es opcional SOLO para el SuperAdmin (id_rol=1).
    La validación de que otros roles tengan hospital se hace en el service.

    Se usa en: POST /api/v1/usuarios
    """
    password:    str      = Field(..., min_length=8, examples=["mipassword123"])
    id_rol:      int      = Field(..., examples=[1])
    id_hospital: int | None = Field(None, examples=[1])


class UsuarioUpdate(BaseModel):
    """
    Datos para actualizar un usuario.
    Todos opcionales. El password se puede cambiar desde aquí también.
    Se usa en: PUT /api/v1/usuarios/{id_usuario}
    """
    nombre:   str | None      = Field(None, min_length=2, max_length=100)
    apellido: str | None      = Field(None, min_length=2, max_length=100)
    email:    EmailStr | None = None
    password: str | None      = Field(None, min_length=8)
    id_rol:   int | None      = None
    activo:   bool | None     = None


class RolEnUsuario(BaseModel):
    """Schema reducido de Rol para embeber dentro de UsuarioResponse."""
    id_rol: int
    nombre: str

    class Config:
        from_attributes = True


class HospitalEnUsuario(BaseModel):
    """Schema reducido de Hospital para embeber dentro de UsuarioResponse."""
    id_hospital: int | None = None
    nombre:      str

    class Config:
        from_attributes = True


class UsuarioResponse(UsuarioBase):
    """
    Datos que devuelve la API al consultar un usuario.
    NO incluye password.

    id_hospital es None para el SuperAdmin.
    hospital es None para el SuperAdmin.

    Se usa en: GET /api/v1/usuarios y GET /api/v1/usuarios/{id_usuario}
    """
    id_usuario:  int
    activo:      bool
    id_rol:      int
    id_hospital: int | None = None

    rol:      RolEnUsuario      | None = None
    hospital: HospitalEnUsuario | None = None

    class Config:
        from_attributes = True