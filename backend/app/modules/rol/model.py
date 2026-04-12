from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Rol(Base):
    __tablename__ = "rol"

    id_rol  = Column(Integer, primary_key=True, index=True)
    nombre  = Column(String(100), nullable=False, unique=True)
    activo  = Column(Boolean, nullable=False, default=True)

    # Relación inversa — cierra el círculo con Usuario.rol
    usuarios = relationship("Usuario", back_populates="rol")
