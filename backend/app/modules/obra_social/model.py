from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class ObraSocial(Base):
    __tablename__ = "obra_social"

    id_obra_social = Column(Integer, primary_key=True, index=True)
    nombre         = Column(String(150), nullable=False, unique=True)
    activo         = Column(Boolean, nullable=False, default=True)

    # Relación inversa
    pacientes = relationship("Paciente", back_populates="obra_social")