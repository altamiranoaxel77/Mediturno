# =============================================================================
# app/database.py — Conexión a PostgreSQL con SQLAlchemy
# =============================================================================
# Responsabilidades de este archivo:
#
#   1. ENGINE     → el "motor" que gestiona el pool de conexiones a PostgreSQL
#   2. SESSION    → fábrica que crea sesiones de base de datos por cada request
#   3. BASE       → clase padre de la que heredan TODOS los modelos SQLAlchemy
#   4. get_db()   → función generadora que FastAPI usa como dependencia
#
# Patrón usado: "session per request"
# Cada petición HTTP abre su propia sesión, la usa y la cierra.
# Así se evitan problemas de concurrencia y conexiones colgadas.
# =============================================================================

from sqlalchemy import create_engine       # Crea el motor de conexión al motor de base de datos
from sqlalchemy.orm import sessionmaker    # Fábrica de sesiones de base de datos
from sqlalchemy.orm import DeclarativeBase # Clase base para los modelos SQLAlchemy (versión moderna)
from sqlalchemy.orm import Session         # Tipo Session, usado para anotaciones de tipo (type hints)
from typing import Generator               # Para tipar correctamente la función generadora get_db

from app.config import settings            # Importa la configuración centralizada (DATABASE_URL, etc.)


# =============================================================================
# 1. Motor de base de datos (Engine)
# =============================================================================
# El engine es el objeto principal de SQLAlchemy. Gestiona un "pool" de
# conexiones abiertas a PostgreSQL, reutilizándolas para mejorar la performance.
#
# No abre una conexión inmediatamente — lo hace de forma lazy cuando se necesita.
#
# pool_pre_ping=True:
#   Antes de entregar una conexión del pool, SQLAlchemy envía un "ping"
#   para verificar que siga activa. Evita el error "server closed the connection
#   unexpectedly" cuando PostgreSQL cierra conexiones inactivas.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)


# =============================================================================
# 2. Fábrica de sesiones (SessionLocal)
# =============================================================================
# SessionLocal NO es una sesión. Es una CLASE que, al instanciarse con (),
# crea una sesión nueva. Por eso se llama en get_db() como: db = SessionLocal()
#
# autocommit=False:
#   Los cambios (INSERT, UPDATE, DELETE) no se guardan automáticamente.
#   Hay que llamar db.commit() explícitamente. Esto nos da control total
#   sobre las transacciones — podemos hacer rollback ante cualquier error.
#
# autoflush=False:
#   SQLAlchemy no envía los cambios pendientes a la BD antes de cada
#   consulta SELECT. Lo manejamos nosotros según necesidad.
#
# bind=engine:
#   Asocia esta fábrica al engine que creamos arriba (nuestra base PostgreSQL).
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# =============================================================================
# 3. Clase base para modelos (Base)
# =============================================================================
# TODOS los modelos del proyecto deben heredar de esta clase.
# SQLAlchemy la usa para rastrear qué clases son modelos y mapearlas a tablas.
#
# Ejemplo de cómo se usa en cada modelo:
#
#   from app.database import Base
#
#   class Hospital(Base):
#       __tablename__ = "hospital"
#       id_hospital = Column(Integer, primary_key=True)
#       nombre      = Column(String, nullable=False)
#
# Alembic también usa esta Base para detectar cambios en los modelos
# y generar automáticamente las migraciones.
class Base(DeclarativeBase):
    pass


# =============================================================================
# 4. Dependencia de sesión para FastAPI (get_db)
# =============================================================================
# Esta función es un GENERADOR que FastAPI inyecta en los endpoints
# mediante el sistema de dependencias (Depends).
#
# Ciclo de vida por cada request HTTP:
#   → FastAPI llama a get_db()
#   → Se crea una sesión nueva: db = SessionLocal()
#   → yield db pausa la función y entrega la sesión al endpoint
#   → El endpoint hace su trabajo usando la sesión
#   → Cuando el endpoint termina (éxito O excepción), finally se ejecuta
#   → db.close() cierra la sesión y devuelve la conexión al pool
#
# El bloque try/finally garantiza que la sesión SIEMPRE se cierre,
# incluso si el endpoint lanza una excepción en el medio.
#
# Cómo usarlo en un router:
# ──────────────────────────
#   from fastapi import Depends
#   from sqlalchemy.orm import Session
#   from app.database import get_db
#
#   @router.get("/pacientes")
#   def listar_pacientes(db: Session = Depends(get_db)):
#       return db.query(Paciente).all()
def get_db() -> Generator[Session, None, None]:
    """
    Generador de sesión de base de datos.

    Abre una sesión por cada request HTTP y la cierra al finalizar,
    sin importar si el request fue exitoso o terminó con error.
    """
    db = SessionLocal()  # Abre una sesión nueva
    try:
        yield db         # Entrega la sesión al endpoint que la pidió
    finally:
        db.close()       # Siempre cierra la sesión al terminar el request