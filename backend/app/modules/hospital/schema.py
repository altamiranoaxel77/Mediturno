# =============================================================================
# modules/hospital/schema.py — Schemas Pydantic para Hospital
# =============================================================================

from pydantic import BaseModel, Field, EmailStr


class HospitalBase(BaseModel):
    """Campos compartidos entre Create y Response."""
    nombre:    str            = Field(..., min_length=2, max_length=200, examples=["Hospital Central"])
    direccion: str | None     = Field(None, max_length=300, examples=["Av. Corrientes 1234"])
    telefono:  str | None     = Field(None, max_length=50,  examples=["0800-333-1234"])
    # EmailStr valida automáticamente que el valor tenga formato de email
    email:     EmailStr | None = Field(None, examples=["contacto@hospital.com"])


class HospitalCreate(HospitalBase):
    """
    Datos para crear un hospital.
    Se usa en: POST /api/v1/hospitales
    """
    pass


class HospitalUpdate(BaseModel):
    """
    Datos para actualizar un hospital.
    Todos opcionales — solo se modifican los campos enviados.
    Se usa en: PUT /api/v1/hospitales/{id_hospital}
    """
    nombre:    str | None      = Field(None, min_length=2, max_length=200)
    direccion: str | None      = Field(None, max_length=300)
    telefono:  str | None      = Field(None, max_length=50)
    email:     EmailStr | None = None
    activo:    bool | None     = None


class HospitalResponse(HospitalBase):
    """
    Datos que devuelve la API al consultar un hospital.
    Se usa en: GET /api/v1/hospitales y GET /api/v1/hospitales/{id_hospital}
    """
    id_hospital: int
    activo:      bool

    class Config:
        from_attributes = True