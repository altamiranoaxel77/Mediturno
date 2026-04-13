# =============================================================================
# modules/especialidad/schema.py — Schemas Pydantic para Especialidad
# =============================================================================

from pydantic import BaseModel, Field


class EspecialidadBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150, examples=["Cardiología"])


class EspecialidadCreate(EspecialidadBase):
    """Se usa en: POST /api/v1/especialidades"""
    pass


class EspecialidadUpdate(BaseModel):
    """Se usa en: PUT /api/v1/especialidades/{id_especialidad}"""
    nombre: str | None  = Field(None, min_length=2, max_length=150)
    activo: bool | None = None


class EspecialidadResponse(EspecialidadBase):
    """Se usa en: GET /api/v1/especialidades"""
    id_especialidad: int
    activo:          bool

    class Config:
        from_attributes = True