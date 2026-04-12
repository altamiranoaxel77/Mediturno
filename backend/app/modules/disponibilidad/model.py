from sqlalchemy import Column, Integer, Boolean, Time, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class DisponibilidadMedico(Base):
    __tablename__ = "disponibilidad_medico"

    # UniqueConstraint → un médico solo puede tener UNA disponibilidad por día y hospital
    # Esto se valida a nivel de base de datos, no solo en el código
    __table_args__ = (
        UniqueConstraint(
            "id_medico", "id_dia", "id_hospital",
            name="uq_disponibilidad_medico_dia_hospital"
        ),
    )

    id_disponibilidad = Column(Integer, primary_key=True, index=True)

    # ── Turno mañana ──────────────────────────────────────────────────────────

    turno_manana       = Column(Boolean, nullable=False, default=False)

    # Solo se completan si turno_manana=True
    hora_inicio_manana = Column(Time, nullable=True)
    hora_fin_manana    = Column(Time, nullable=True)

    # ── Turno tarde ───────────────────────────────────────────────────────────

    turno_tarde        = Column(Boolean, nullable=False, default=False)

    # Solo se completan si turno_tarde=True
    hora_inicio_tarde  = Column(Time, nullable=True)
    hora_fin_tarde     = Column(Time, nullable=True)

    # ── Configuración ─────────────────────────────────────────────────────────

    # Duración de cada turno en minutos
    # Ejemplo: duracion=30 → slots cada 30 min → 08:00, 08:30, 09:00...
    duracion_turno_minutos = Column(Integer, nullable=False, default=30)

    activo = Column(Boolean, nullable=False, default=True)

    # ── Claves foráneas ───────────────────────────────────────────────────────

    # CASCADE → si se elimina el médico, se eliminan sus disponibilidades
    id_medico   = Column(Integer, ForeignKey("medico.id_medico",       ondelete="CASCADE"),   nullable=False)
    id_dia      = Column(Integer, ForeignKey("dia_semana.id_dia",      ondelete="RESTRICT"),  nullable=False)
    id_hospital = Column(Integer, ForeignKey("hospital.id_hospital",   ondelete="RESTRICT"),  nullable=False)

    # ── Relaciones ────────────────────────────────────────────────────────────

    medico   = relationship("Medico",    back_populates="disponibilidades", lazy="joined")
    dia      = relationship("DiaSemana", back_populates="disponibilidades", lazy="joined")
    hospital = relationship("Hospital",  back_populates="disponibilidades", lazy="joined")