# =============================================================================
# modules/usuario/model.py — Modelo SQLAlchemy para la tabla "usuario"
# =============================================================================
# El SuperAdmin (id_rol=1) NO pertenece a ningún hospital — id_hospital es NULL.
# Todos los demás roles DEBEN tener un hospital asignado.
# Esta regla se garantiza con un CHECK CONSTRAINT en la base de datos.
# =============================================================================

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    # CHECK CONSTRAINT a nivel de base de datos:
    # Solo el rol 1 (SuperAdmin) puede tener id_hospital en NULL.
    # Cualquier otro rol DEBE tener un hospital asignado.
    # Esto garantiza integridad de datos incluso si alguien accede directo a la BD.
    __table_args__ = (
        CheckConstraint(
            "(id_rol = 1) OR (id_hospital IS NOT NULL)",
            name="chk_hospital_superadmin"
        ),
    )

    # ── Columnas ──────────────────────────────────────────────────────────────

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre     = Column(String(100), nullable=False)
    apellido   = Column(String(100), nullable=False)

    # DNI único a nivel global
    dni   = Column(String(20),  nullable=False, unique=True)

    # Email único — se usa como identificador de login
    email = Column(String(150), nullable=False, unique=True)

    # Siempre se guarda el HASH de bcrypt, NUNCA la contraseña en texto plano
    password = Column(String(255), nullable=False)

    activo = Column(Boolean, nullable=False, default=True)

    # ── Claves foráneas ───────────────────────────────────────────────────────

    # FK hacia "rol" — define los permisos del usuario
    id_rol = Column(
        Integer,
        ForeignKey("rol.id_rol", ondelete="RESTRICT"),
        nullable=False
    )

    # FK hacia "hospital" — nullable=True porque el SuperAdmin no tiene hospital
    # El CHECK CONSTRAINT de arriba garantiza que solo el SuperAdmin pueda ser NULL
    id_hospital = Column(
        Integer,
        ForeignKey("hospital.id_hospital", ondelete="RESTRICT"),
        nullable=True   # NULL solo para SuperAdmin (id_rol=1)
    )

    # ── Relaciones ORM ────────────────────────────────────────────────────────

    rol      = relationship("Rol",      back_populates="usuarios", lazy="joined")
    hospital = relationship("Hospital", back_populates="usuarios", lazy="joined")

    # Relación inversa con Medico (1 a 1)
    medico = relationship("Medico", back_populates="usuario", uselist=False)