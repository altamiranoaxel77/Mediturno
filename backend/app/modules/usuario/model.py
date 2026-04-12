from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre     = Column(String(100), nullable=False)
    apellido   = Column(String(100), nullable=False)

    # DNI único a nivel global — una persona = un DNI
    dni        = Column(String(20), nullable=False, unique=True)

    # Email único — se usa como identificador de login
    email      = Column(String(150), nullable=False, unique=True)

    # Siempre se guarda el HASH de bcrypt, nunca la contraseña en texto plano
    password   = Column(String(255), nullable=False)

    activo     = Column(Boolean, nullable=False, default=True)

    # ── Claves foráneas ───────────────────────────────────────────────────────

    # ondelete="RESTRICT" → no se puede eliminar un Rol si tiene usuarios asignados
    id_rol      = Column(Integer, ForeignKey("rol.id_rol",           ondelete="RESTRICT"), nullable=False)
    id_hospital = Column(Integer, ForeignKey("hospital.id_hospital", ondelete="RESTRICT"), nullable=False)

    # ── Relaciones ────────────────────────────────────────────────────────────

    # lazy="joined" → carga el rol y hospital en la misma query (evita N+1 queries)
    rol      = relationship("Rol",      back_populates="usuarios", lazy="joined")
    hospital = relationship("Hospital", back_populates="usuarios", lazy="joined")

    # Relación inversa con Medico (1 a 1 — un usuario puede ser médico)
    medico = relationship("Medico", back_populates="usuario", uselist=False)