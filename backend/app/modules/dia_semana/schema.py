# =============================================================================
# modules/dia_semana/schema.py — Schemas Pydantic para DiaSemana
# =============================================================================
# DiaSemana es una tabla de referencia con datos fijos (Lunes a Domingo).
# Solo necesita schema de respuesta — no se crea ni modifica desde la API.
# =============================================================================

from pydantic import BaseModel, Field


class DiaSemanaResponse(BaseModel):
    """
    Datos que devuelve la API al consultar los días de la semana.
    Esta tabla es de solo lectura — sus datos se cargan una sola vez.
    Se usa en: GET /api/v1/dias-semana
    """
    id_dia: int
    nombre: str = Field(..., examples=["Lunes"])

    class Config:
        from_attributes = True