# =============================================================================
# modules/turno/schema.py — Schemas Pydantic para Turno
# =============================================================================

from pydantic import BaseModel, Field, model_validator
from datetime import date, time, datetime
from typing import Literal


# Tipo que restringe los valores válidos del estado del turno.
# Si el frontend envía un valor distinto, Pydantic rechaza la petición
# antes de que llegue al service.
EstadoTurno = Literal["pendiente", "atendido", "cancelado", "ausente"]


class TurnoCreate(BaseModel):
    """
    Datos para registrar un nuevo turno.
    hora_fin NO se envía — se calcula automáticamente en el service
    según la duracion_turno_minutos de la disponibilidad del médico.
    Se usa en: POST /api/v1/turnos
    """
    fecha:           date = Field(..., examples=["2025-08-15"])
    hora:            time = Field(..., examples=["09:00:00"])
    id_paciente:     int  = Field(..., examples=[1])
    id_medico:       int  = Field(..., examples=[1])
    id_hospital:     int  = Field(..., examples=[1])

    # Opcional — el paciente o recepcionista puede indicar el motivo
    motivo_consulta: str | None = Field(None, max_length=500, examples=["Control de rutina"])


class TurnoUpdate(BaseModel):
    """
    Datos para actualizar información de un turno.
    Solo permite modificar campos no críticos.
    Para cambiar el estado se usa TurnoActualizarEstado.
    Se usa en: PUT /api/v1/turnos/{id_turno}
    """
    motivo_consulta: str | None = Field(None, max_length=500)
    observaciones:   str | None = Field(None, max_length=1000)


class TurnoActualizarEstado(BaseModel):
    """
    Schema exclusivo para cambiar el estado de un turno.
    Separado de TurnoUpdate para hacer explícito que cambiar el estado
    es una operación con sus propias reglas de negocio.
    Se usa en: PUT /api/v1/turnos/{id_turno}/estado
    """
    estado: EstadoTurno = Field(..., examples=["atendido"])

    # Observaciones opcionales — el médico puede agregar notas al cerrar el turno
    observaciones: str | None = Field(None, max_length=1000)


# ── Schemas reducidos para anidar en TurnoResponse ────────────────────────────

class PacienteEnTurno(BaseModel):
    """Datos mínimos del paciente para mostrar en la respuesta del turno."""
    id_paciente: int
    nombre:      str
    apellido:    str
    dni:         str

    class Config:
        from_attributes = True


class MedicoEnTurno(BaseModel):
    """Datos mínimos del médico para mostrar en la respuesta del turno."""
    id_medico: int
    matricula: str

    class Config:
        from_attributes = True


class TurnoResponse(BaseModel):
    """
    Datos que devuelve la API al consultar un turno.
    Incluye paciente y médico anidados para que el frontend
    pueda mostrar los datos completos sin llamadas adicionales.
    Se usa en: GET /api/v1/turnos y GET /api/v1/turnos/{id_turno}
    """
    id_turno:        int
    fecha:           date
    hora:            time
    hora_fin:        time
    estado:          EstadoTurno
    motivo_consulta: str | None
    observaciones:   str | None
    id_paciente:     int
    id_medico:       int
    id_hospital:     int
    creado_en:       datetime
    actualizado_en:  datetime

    paciente: PacienteEnTurno | None = None
    medico:   MedicoEnTurno   | None = None

    class Config:
        from_attributes = True


class SlotDisponible(BaseModel):
    """
    Representa un horario disponible para sacar turno.
    Se devuelve en GET /api/v1/turnos/disponibles?id_medico=X&fecha=YYYY-MM-DD
    El frontend muestra estos slots para que el usuario elija uno.
    """
    hora:     time = Field(..., examples=["09:00:00"])
    hora_fin: time = Field(..., examples=["09:30:00"])