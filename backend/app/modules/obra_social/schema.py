# =============================================================================
# modules/obra_social/schema.py — Schemas Pydantic para ObraSocial
# =============================================================================

from pydantic import BaseModel, Field


class ObraSocialBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150, examples=["OSDE"])


class ObraSocialCreate(ObraSocialBase):
    """Se usa en: POST /api/v1/obras-sociales"""
    pass


class ObraSocialUpdate(BaseModel):
    """Se usa en: PUT /api/v1/obras-sociales/{id_obra_social}"""
    nombre: str | None  = Field(None, min_length=2, max_length=150)
    activo: bool | None = None


class ObraSocialResponse(ObraSocialBase):
    """Se usa en: GET /api/v1/obras-sociales"""
    id_obra_social: int
    activo:         bool

    class Config:
        from_attributes = True