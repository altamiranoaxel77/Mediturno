from sqlalchemy import Column, Integer, String, Boolean, Date, Time, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func   # func.now() → genera el timestamp actual en PostgreSQL
from app.database import Base


class Turno(Base):
    __tablename__ = "turno"

    id_turno = Column(Integer, primary_key=True, index=True)

    # Index=True → las consultas más frecuentes filtran por fecha
    fecha    = Column(Date, nullable=False, index=True)
    hora     = Column(Time, nullable=False)

    # hora_fin se calcula al crear el turno según duracion_turno_minutos
    hora_fin = Column(Time, nullable=False)

    # Estado del turno — valores posibles:
    # "pendiente" | "atendido" | "cancelado" | "ausente"
    estado   = Column(String(50), nullable=False, default="pendiente")

    # Opcionales — se completan antes o durante la consulta
    motivo_consulta = Column(String(500),  nullable=True)
    observaciones   = Column(String(1000), nullable=True)

    # ── Auditoría ─────────────────────────────────────────────────────────────

    # server_default=func.now() → PostgreSQL asigna el timestamp automáticamente al insertar
    # onupdate=func.now()       → PostgreSQL actualiza el timestamp en cada modificación
    creado_en      = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # ── Claves foráneas ───────────────────────────────────────────────────────

    # Index=True en id_paciente e id_medico → se filtran frecuentemente en consultas
    id_paciente = Column(Integer, ForeignKey("paciente.id_paciente", ondelete="RESTRICT"), nullable=False, index=True)
    id_medico   = Column(Integer, ForeignKey("medico.id_medico",     ondelete="RESTRICT"), nullable=False, index=True)
    id_hospital = Column(Integer, ForeignKey("hospital.id_hospital", ondelete="RESTRICT"), nullable=False)

    # ── Relaciones ────────────────────────────────────────────────────────────

    paciente = relationship("Paciente", back_populates="turnos", lazy="joined")
    medico   = relationship("Medico",   back_populates="turnos", lazy="joined")
    hospital = relationship("Hospital", back_populates="turnos", lazy="joined")