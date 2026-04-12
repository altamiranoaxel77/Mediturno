from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Especialidad(Base):
    __tablename__ = "especialidad"

    id_especialidad = Column(Integer, primary_key=True, index=True)
    nombre          = Column(String(150), nullable=False, unique=True)
    activo          = Column(Boolean, nullable=False, default=True)

    # Relación inversa
    medicos = relationship("Medico", back_populates="especialidad")