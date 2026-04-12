from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Medico(Base):
    __tablename__ = "medico"

    id_medico = Column(Integer, primary_key=True, index=True)

    # Matrícula profesional — única e irrepetible
    matricula = Column(String(50), nullable=False, unique=True)

    activo    = Column(Boolean, nullable=False, default=True)

    # ── Claves foráneas ───────────────────────────────────────────────────────

    # unique=True → un usuario no puede estar asociado a dos médicos (relación 1 a 1)
    id_usuario      = Column(Integer, ForeignKey("usuario.id_usuario",           ondelete="RESTRICT"), nullable=False, unique=True)
    id_especialidad = Column(Integer, ForeignKey("especialidad.id_especialidad", ondelete="RESTRICT"), nullable=False)
    id_hospital     = Column(Integer, ForeignKey("hospital.id_hospital",         ondelete="RESTRICT"), nullable=False)

    # ── Relaciones ────────────────────────────────────────────────────────────

    usuario      = relationship("Usuario",      back_populates="medico",        lazy="joined")
    especialidad = relationship("Especialidad", back_populates="medicos",       lazy="joined")
    hospital     = relationship("Hospital",     back_populates="medicos",       lazy="joined")

    # lazy="dynamic" → no carga todos los registros hasta que se acceda explícitamente
    # Útil cuando un médico puede tener cientos de turnos
    disponibilidades = relationship("DisponibilidadMedico", back_populates="medico", lazy="dynamic")
    turnos           = relationship("Turno",                back_populates="medico", lazy="dynamic")