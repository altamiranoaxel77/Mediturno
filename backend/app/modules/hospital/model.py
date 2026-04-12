from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Hospital(Base):
    __tablename__ = "hospital"

    id_hospital = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String(200), nullable=False)
    direccion   = Column(String(300), nullable=True)
    telefono    = Column(String(50),  nullable=True)
    email       = Column(String(150), nullable=True)
    activo      = Column(Boolean, nullable=False, default=True)

    # Relaciones inversas
    usuarios         = relationship("Usuario",              back_populates="hospital")
    medicos          = relationship("Medico",               back_populates="hospital")
    pacientes        = relationship("Paciente",             back_populates="hospital")
    disponibilidades = relationship("DisponibilidadMedico", back_populates="hospital")
    turnos           = relationship("Turno",                back_populates="hospital")