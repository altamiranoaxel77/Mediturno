# =============================================================================
# modules/paciente/schema.py — Schemas Pydantic para Paciente
# =============================================================================

from pydantic import BaseModel, Field, EmailStr
from datetime import date


class PacienteBase(BaseModel):
    """Campos base del paciente."""
    nombre:           str           = Field(..., min_length=2, max_length=100, examples=["María"])
    apellido:         str           = Field(..., min_length=2, max_length=100, examples=["López"])
    dni:              str           = Field(..., min_length=7, max_length=20,  examples=["28456789"])
    telefono:         str | None    = Field(None, max_length=50,               examples=["3413001234"])
    email:            EmailStr | None = Field(None,                            examples=["maria@email.com"])
    fecha_nacimiento: date | None   = Field(None,                              examples=["1990-05-20"])


class PacienteCreate(PacienteBase):
    """
    Datos para crear un paciente.
    id_obra_social es opcional — puede ser paciente particular (None).
    Se usa en: POST /api/v1/pacientes
    """
    id_obra_social: int | None = Field(None, examples=[1])
    id_hospital:    int        = Field(...,  examples=[1])


class PacienteUpdate(BaseModel):
    """
    Datos para actualizar un paciente.
    Todos opcionales — solo se modifican los campos enviados.
    Se usa en: PUT /api/v1/pacientes/{id_paciente}
    """
    nombre:           str | None      = Field(None, min_length=2, max_length=100)
    apellido:         str | None      = Field(None, min_length=2, max_length=100)
    telefono:         str | None      = Field(None, max_length=50)
    email:            EmailStr | None = None
    fecha_nacimiento: date | None     = None
    id_obra_social:   int | None      = None


class PacienteDesactivar(BaseModel):
    """
    Schema para la baja lógica del paciente.
    Se usa en: PUT /api/v1/pacientes/{id_paciente}/desactivar
    """
    activo: bool = False


# ── Schema reducido para anidar dentro de otras respuestas ────────────────────

class ObraSocialEnPaciente(BaseModel):
    """Datos de la obra social para mostrar en la respuesta del paciente."""
    id_obra_social: int
    nombre:         str

    class Config:
        from_attributes = True


class PacienteResponse(PacienteBase):
    """
    Datos que devuelve la API al consultar un paciente.
    Incluye la obra social anidada si tiene una asignada.
    Se usa en: GET /api/v1/pacientes y GET /api/v1/pacientes/{id_paciente}
    """
    id_paciente:    int
    activo:         bool
    id_hospital:    int
    id_obra_social: int | None = None

    # Objeto anidado — si el paciente tiene obra social, devuelve su nombre
    # Si es particular, obra_social será None
    obra_social: ObraSocialEnPaciente | None = None

    class Config:
        from_attributes = True


class PacienteResumen(BaseModel):
    """
    Schema reducido de Paciente para anidar dentro de TurnoResponse.
    Solo los datos necesarios para identificar al paciente en un turno.
    """
    id_paciente: int
    nombre:      str
    apellido:    str
    dni:         str

    class Config:
        from_attributes = True