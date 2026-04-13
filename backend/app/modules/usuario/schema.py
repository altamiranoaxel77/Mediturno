# =============================================================================
# modules/usuario/schema.py — Schemas Pydantic para Usuario
# =============================================================================
# REGLA DE ORO: la contraseña entra en UsuarioCreate pero NUNCA
# sale en UsuarioResponse. Pydantic lo garantiza porque UsuarioResponse
# no tiene el campo password definido.
# =============================================================================

from pydantic import BaseModel, Field, EmailStr


class UsuarioBase(BaseModel):
    """Campos compartidos entre Create y Response (sin password)."""
    nombre:   str      = Field(..., min_length=2, max_length=100,  examples=["Juan"])
    apellido: str      = Field(..., min_length=2, max_length=100,  examples=["García"])
    dni:      str      = Field(..., min_length=7, max_length=20,   examples=["30123456"])
    email:    EmailStr = Field(...,                                 examples=["juan@hospital.com"])


class UsuarioCreate(UsuarioBase):
    """
    Datos para crear un usuario.
    Incluye password — es el ÚNICO schema donde existe este campo.
    Se usa en: POST /api/v1/usuarios
    """
    # min_length=8 fuerza contraseñas de al menos 8 caracteres
    password:    str = Field(..., min_length=8, examples=["mipassword123"])
    id_rol:      int = Field(..., examples=[1])
    id_hospital: int = Field(..., examples=[1])


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
    """
    Schema reducido de Rol para embeber dentro de UsuarioResponse.
    Solo devolvemos lo que el frontend necesita mostrar — no todo el objeto.
    """
    id_rol: int
    nombre: str

    class Config:
        from_attributes = True


class HospitalEnUsuario(BaseModel):
    """Schema reducido de Hospital para embeber dentro de UsuarioResponse."""
    id_hospital: int
    nombre:      str

    class Config:
        from_attributes = True


class UsuarioResponse(UsuarioBase):
    """
    Datos que devuelve la API al consultar un usuario.
    NO incluye password — Pydantic omite automáticamente los campos
    que no están definidos en este schema.

    Incluye los objetos relacionados (rol y hospital) para que el frontend
    no tenga que hacer llamadas adicionales para obtener esos datos.

    Se usa en: GET /api/v1/usuarios y GET /api/v1/usuarios/{id_usuario}
    """
    id_usuario:  int
    activo:      bool
    id_rol:      int
    id_hospital: int

    # Objetos anidados — el frontend recibe el nombre del rol y hospital
    # directamente en la misma respuesta, sin necesitar otra llamada a la API
    rol:      RolEnUsuario      | None = None
    hospital: HospitalEnUsuario | None = None

    class Config:
        from_attributes = True