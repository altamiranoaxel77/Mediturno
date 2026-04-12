from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class DiaSemana(Base):
    __tablename__ = "dia_semana"

    # Convenio: 1=Lunes, 2=Martes, 3=Miércoles, 4=Jueves,
    #           5=Viernes, 6=Sábado, 7=Domingo
    id_dia = Column(Integer, primary_key=True)
    nombre = Column(String(20), nullable=False, unique=True)

    # Relación inversa
    disponibilidades = relationship("DisponibilidadMedico", back_populates="dia")