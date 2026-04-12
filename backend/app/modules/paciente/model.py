from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Paciente(Base):
    __tablename__ = "paciente"

    id_paciente = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String(100), nullable=False)
    apellido    = Column(String(100), nullable=False)

    # Index=True porque se busca frecuentemente por DNI
    dni         = Column(String(20), nullable=False, index=True)

    telefono    = Column(String(50),  nullable=True)
    email       = Column(String(150), nullable=True)

    # Date → mapea al tipo DATE de PostgreSQL
    fecha_nacimiento = Column(Date, nullable=True)

    activo      = Column(Boolean, nullable=False, default=True)

    # ── Claves foráneas ───────────────────────────────────────────────────────

    # nullable=True → el paciente puede ser particular (sin obra social)
    # ondelete="SET NULL" → si se elimina la obra social, el campo queda en NULL
    id_obra_social = Column(Integer, ForeignKey("obra_social.id_obra_social", ondelete="SET NULL"),  nullable=True)
    id_hospital    = Column(Integer, ForeignKey("hospital.id_hospital",       ondelete="RESTRICT"), nullable=False)

    # ── Relaciones ────────────────────────────────────────────────────────────

    obra_social = relationship("ObraSocial", back_populates="pacientes", lazy="joined")
    hospital    = relationship("Hospital",   back_populates="pacientes", lazy="joined")

    # Un paciente puede tener muchos turnos a lo largo del tiempo
    turnos = relationship("Turno", back_populates="paciente", lazy="dynamic")