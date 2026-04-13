# =============================================================================
# modules/rol/schema.py — Schemas Pydantic para Rol
# =============================================================================

from pydantic import BaseModel, Field

class RolBase(BaseModel):
    """
    Campos compartidos entre Create y Response.
    Evita repetir los mismos campos en cada schema.
    """
    # Field(...) significa que el campo es obligatorio
    # min_length/max_length validan la longitud antes de llegar al service
    nombre: str = Field(..., min_length=2, max_length=100, examples=["Administrador"])

class RolCreate(RolBase):
    """
    Datos necesarios para crear un rol.
    Hereda nombre de RolBase.
    Se usa en: POST /api/v1/roles
    """
    pass

class RolUpdate(BaseModel):
    """
    Datos para actualizar un rol.
    Todos los campos son opcionales — solo se actualizan los que se envían.
    Se usa en: PUT /api/v1/roles/{id_rol}
    """
    nombre: str | None = Field(None, min_length=2, max_length=100)
    activo: bool | None = None


class RolResponse(RolBase):
    """
    Datos que devuelve la API al consultar un rol.
    Incluye id y activo que no están en Create.
    Se usa en: GET /api/v1/roles y GET /api/v1/roles/{id_rol}
    """
    id_rol: int
    activo: bool

    class Config:
        # from_attributes=True permite que Pydantic lea los datos
        # directamente desde un objeto SQLAlchemy (no solo desde dicts)
        from_attributes = True
