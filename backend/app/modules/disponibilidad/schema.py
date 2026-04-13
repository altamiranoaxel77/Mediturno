# =============================================================================
# modules/disponibilidad/schema.py — Schemas Pydantic para DisponibilidadMedico
# =============================================================================

from pydantic import BaseModel, Field, model_validator
from datetime import time


class DisponibilidadBase(BaseModel):
    """Campos base de la disponibilidad."""

    # ── Turno mañana ──────────────────────────────────────────────────────────
    turno_manana:       bool        = Field(False, examples=[True])
    hora_inicio_manana: time | None = Field(None,  examples=["08:00:00"])
    hora_fin_manana:    time | None = Field(None,  examples=["12:00:00"])

    # ── Turno tarde ───────────────────────────────────────────────────────────
    turno_tarde:        bool        = Field(False, examples=[True])
    hora_inicio_tarde:  time | None = Field(None,  examples=["15:00:00"])
    hora_fin_tarde:     time | None = Field(None,  examples=["19:00:00"])

    # Duración de cada slot en minutos
    duracion_turno_minutos: int = Field(30, ge=10, le=120, examples=[30])
    # ge=10 → mínimo 10 minutos | le=120 → máximo 2 horas

    @model_validator(mode="after")
    def validar_horarios(self):
        """
        Validación de negocio a nivel de schema:
        Si se activa un turno, sus horarios son obligatorios.
        Si no se activa, no deben enviarse horarios.

        Esto es una validación temprana — la validación profunda
        (superposición con otros turnos) se hace en el service.
        """
        if self.turno_manana:
            if not self.hora_inicio_manana or not self.hora_fin_manana:
                raise ValueError(
                    "Si turno_manana es True, hora_inicio_manana y hora_fin_manana son obligatorios."
                )
            if self.hora_inicio_manana >= self.hora_fin_manana:
                raise ValueError(
                    "hora_inicio_manana debe ser anterior a hora_fin_manana."
                )

        if self.turno_tarde:
            if not self.hora_inicio_tarde or not self.hora_fin_tarde:
                raise ValueError(
                    "Si turno_tarde es True, hora_inicio_tarde y hora_fin_tarde son obligatorios."
                )
            if self.hora_inicio_tarde >= self.hora_fin_tarde:
                raise ValueError(
                    "hora_inicio_tarde debe ser anterior a hora_fin_tarde."
                )

        if not self.turno_manana and not self.turno_tarde:
            raise ValueError(
                "Debe activarse al menos un turno: turno_manana o turno_tarde."
            )

        return self


class DisponibilidadCreate(DisponibilidadBase):
    """
    Datos para crear la disponibilidad de un médico en un día.
    Se usa en: POST /api/v1/disponibilidad
    """
    id_medico:   int = Field(..., examples=[1])
    id_dia:      int = Field(..., ge=1, le=7, examples=[1])
    # ge=1 le=7 → solo acepta valores del 1 (Lunes) al 7 (Domingo)
    id_hospital: int = Field(..., examples=[1])


class DisponibilidadUpdate(BaseModel):
    """
    Datos para modificar la disponibilidad de un médico.
    Todos opcionales.
    Se usa en: PUT /api/v1/disponibilidad/{id_disponibilidad}
    """
    turno_manana:           bool | None = None
    hora_inicio_manana:     time | None = None
    hora_fin_manana:        time | None = None
    turno_tarde:            bool | None = None
    hora_inicio_tarde:      time | None = None
    hora_fin_tarde:         time | None = None
    duracion_turno_minutos: int | None  = Field(None, ge=10, le=120)


# ── Schemas reducidos para anidar en DisponibilidadResponse ───────────────────

class DiaSemanaEnDisponibilidad(BaseModel):
    id_dia: int
    nombre: str

    class Config:
        from_attributes = True


class MedicoEnDisponibilidad(BaseModel):
    id_medico: int
    matricula: str

    class Config:
        from_attributes = True


class DisponibilidadResponse(DisponibilidadBase):
    """
    Datos que devuelve la API al consultar la disponibilidad de un médico.
    Se usa en: GET /api/v1/disponibilidad y GET /api/v1/disponibilidad/{id}
    """
    id_disponibilidad: int
    activo:            bool
    id_medico:         int
    id_dia:            int
    id_hospital:       int

    # Objetos anidados para que el frontend muestre el nombre del día
    # y los datos del médico sin llamadas adicionales
    dia:    DiaSemanaEnDisponibilidad | None = None
    medico: MedicoEnDisponibilidad    | None = None

    class Config:
        from_attributes = True