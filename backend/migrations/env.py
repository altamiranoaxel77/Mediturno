# =============================================================================
# migrations/env.py — Configuración de Alembic
# =============================================================================
# Este archivo controla cómo Alembic se conecta a la base de datos
# y detecta los cambios en los modelos.
#
# IMPORTANTE: la URL de conexión se lee desde el archivo .env a través
# de config.py — nunca se hardcodea aquí ni en alembic.ini.
# =============================================================================

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# ── Importar configuración del proyecto ───────────────────────────────────────
# Lee la DATABASE_URL desde el archivo .env
from app.config import settings

# ── Importar Base y todos los modelos ─────────────────────────────────────────
# Alembic necesita que todos los modelos estén importados aquí para detectar
# cambios y generar migraciones automáticamente.
# Si agregás un modelo nuevo, importalo en esta sección.
from app.database import Base

from app.modules.rol.model            import Rol               # noqa: F401
from app.modules.hospital.model       import Hospital          # noqa: F401
from app.modules.especialidad.model   import Especialidad      # noqa: F401
from app.modules.obra_social.model    import ObraSocial        # noqa: F401
from app.modules.dia_semana.model     import DiaSemana         # noqa: F401
from app.modules.usuario.model        import Usuario           # noqa: F401
from app.modules.medico.model         import Medico            # noqa: F401
from app.modules.paciente.model       import Paciente          # noqa: F401
from app.modules.disponibilidad.model import DisponibilidadMedico  # noqa: F401
from app.modules.turno.model          import Turno             # noqa: F401

# ── Configuración de Alembic ──────────────────────────────────────────────────
config = context.config

# Interpreta el archivo de logging definido en alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Le pasamos el metadata de nuestra Base para que Alembic
# pueda comparar el estado actual de los modelos contra la BD
target_metadata = Base.metadata

# ── Inyectar la DATABASE_URL desde el .env ────────────────────────────────────
# Esto sobreescribe el valor de sqlalchemy.url del alembic.ini
# con la URL real leída desde nuestras variables de entorno.
# Así nunca hay contraseñas hardcodeadas en el repositorio.
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


# =============================================================================
# Funciones de migración — NO modificar
# =============================================================================

def run_migrations_offline() -> None:
    """
    Ejecuta migraciones en modo 'offline' (sin conexión activa a la BD).
    Genera el SQL puro para ejecutarlo manualmente si se necesita.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Ejecuta migraciones en modo 'online' (con conexión activa a la BD).
    Es el modo que se usa normalmente con: alembic upgrade head
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# Detecta automáticamente si correr en modo online u offline
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()