# =============================================================================
# app/config.py — Configuración central de la aplicación
# =============================================================================
# Responsabilidad: leer las variables del archivo .env y exponerlas
# como un objeto tipado accesible desde cualquier parte del proyecto.
#
# ¿Por qué pydantic-settings?
# Porque valida los tipos automáticamente y lanza un error descriptivo
# si falta alguna variable obligatoria, en lugar de fallar en otro lado.
# =============================================================================

from pydantic_settings import BaseSettings  # Lee y valida variables de entorno
from functools import lru_cache             # Cachea la instancia para no releer el .env en cada llamada


class Settings(BaseSettings):
    """
    Clase que representa TODA la configuración de la aplicación.

    Cada atributo se mapea directamente a una variable del archivo .env.
    Si una variable no tiene valor por defecto y no está en el .env,
    la aplicación lanza un error al iniciar — comportamiento deseado,
    porque es mejor fallar al arrancar que fallar en producción.
    """

    # ── Conexión a la base de datos ───────────────────────────────────────────
    # Formato completo:
    # postgresql+psycopg2://USUARIO:CONTRASEÑA@HOST:PUERTO/NOMBRE_BASE_DE_DATOS
    #
    # Ejemplo real:
    # postgresql+psycopg2://postgres:admin123@localhost:5432/mediturno
    DATABASE_URL: str

    # ── Seguridad / JWT ───────────────────────────────────────────────────────
    # Clave secreta para firmar los tokens JWT. Debe ser larga y aleatoria.
    # Generá una con: python -c "import secrets; print(secrets.token_hex(32))"
    # NUNCA subas este valor al repositorio.
    SECRET_KEY: str

    # Algoritmo criptográfico para firmar el token.
    # HS256 (HMAC-SHA256) es el estándar más usado para APIs internas.
    ALGORITHM: str = "HS256"

    # Tiempo en minutos hasta que el token expira y el usuario debe volver a loguearse.
    # 60 = 1 hora. Ajustá según las necesidades del sistema.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ── Entorno de ejecución ──────────────────────────────────────────────────
    # Controla comportamientos que difieren entre desarrollo y producción,
    # como mostrar u ocultar la documentación de Swagger.
    # Valores válidos: "development" | "production"
    ENVIRONMENT: str = "development"

    # ── Metadatos del proyecto (opcionales pero útiles) ───────────────────────
    APP_NAME: str = "Mediturno API"
    APP_VERSION: str = "1.0.0"

    class Config:
        # Le indica a pydantic-settings dónde está el archivo de variables de entorno
        env_file = ".env"

        # Hace que los nombres de variables sean case-insensitive:
        # DATABASE_URL y database_url se tratan como la misma variable
        case_sensitive = False


# =============================================================================
# Función de acceso a la configuración
# =============================================================================

@lru_cache()
def get_settings() -> Settings:
    """
    Retorna la instancia única y cacheada de la configuración.

    @lru_cache garantiza que el archivo .env se lea UNA SOLA VEZ
    durante toda la vida del proceso. Las llamadas siguientes devuelven
    la misma instancia desde memoria, sin volver a leer el disco.

    Uso recomendado (como dependencia en FastAPI):
    ─────────────────────────────────────────────
        from fastapi import Depends
        from app.config import get_settings, Settings

        @router.get("/algo")
        def mi_endpoint(settings: Settings = Depends(get_settings)):
            print(settings.DATABASE_URL)

    Uso directo (en módulos que no son endpoints):
    ──────────────────────────────────────────────
        from app.config import settings
        print(settings.DATABASE_URL)
    """
    return Settings()


# Instancia global lista para importar directamente.
# La mayoría de los módulos usarán esta línea:
#   from app.config import settings
settings = get_settings()