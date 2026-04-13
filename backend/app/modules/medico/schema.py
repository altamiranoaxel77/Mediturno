# =============================================================================
# modules/medico/schema.py — Schemas Pydantic para Medico
# =============================================================================

from pydantic import BaseModel, Field


class MedicoBase(BaseModel):
    """Campos base del médico."""
    matricula: str = Field(..., min_length=2, max_length=50, examples=["MP-12345"])


class MedicoCreate(MedicoBase):
    """
    Datos para crear un médico.
    Requiere un id_usuario existente — el médico debe tener cuenta de usuario.
    Se usa en: POST /api/v1/medicos
    """
    id_usuario:      int = Field(..., examples=[3])
    id_especialidad: int = Field(..., examples=[1])
    id_hospital:     int = Field(..., examples=[1])


class MedicoUpdate(BaseModel):
    """
    Datos para actualizar un médico.
    Se usa en: PUT /api/v1/medicos/{id_medico}
    """
    matricula:       str | None  = Field(None, min_length=2, max_length=50)
    id_especialidad: int | None  = None
    activo:          bool | None = None


# ── Schemas reducidos para anidar en MedicoResponse ───────────────────────────

class UsuarioEnMedico(BaseModel):
    """Datos del usuario asociado al médico para mostrar en la respuesta."""
    id_usuario: int
    nombre:     str
    apellido:   str
    email:      str

    class Config:
        from_attributes = True


class EspecialidadEnMedico(BaseModel):
    """Datos de la especialidad para mostrar en la respuesta del médico."""
    id_especialidad: int
    nombre:          str

    class Config:
        from_attributes = True


class HospitalEnMedico(BaseModel):
    """Datos del hospital para mostrar en la respuesta del médico."""
    id_hospital: int
    nombre:      str

    class Config:
        from_attributes = True


class MedicoResponse(MedicoBase):
    """
    Datos que devuelve la API al consultar un médico.
    Incluye los datos del usuario, especialidad y hospital anidados
    para que el frontend pueda mostrar el nombre completo del médico
    sin necesitar llamadas adicionales.

    Se usa en: GET /api/v1/medicos y GET /api/v1/medicos/{id_medico}
    """
    id_medico:       int
    activo:          bool
    id_usuario:      int
    id_especialidad: int
    id_hospital:     int

    usuario:      UsuarioEnMedico      | None = None
    especialidad: EspecialidadEnMedico | None = None
    hospital:     HospitalEnMedico     | None = None

    class Config:
        from_attributes = True