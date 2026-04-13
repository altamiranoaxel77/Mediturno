# =============================================================================
# app/main.py — Punto de entrada de la aplicación FastAPI
# =============================================================================
# Este archivo es el corazón del backend. Aquí se:
#
#   1. Crea la instancia principal de FastAPI (la app)
#   2. Configura CORS para que Vue.js pueda comunicarse con la API
#   3. Registran todos los routers de cada módulo
#   4. Define los endpoints básicos de health check
#
# Para iniciar el servidor en desarrollo:
#   uvicorn app.main:app --reload --port 8000
#
# Documentación automática disponible en:
#   http://localhost:8000/docs   → Swagger UI (interfaz visual)
#   http://localhost:8000/redoc  → ReDoc (documentación alternativa)
# =============================================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
import app.models  # noqa: F401 — carga todos los modelos en memoria

# =============================================================================
# Instancia principal de FastAPI
# =============================================================================
# FastAPI genera automáticamente la documentación interactiva a partir
# de los tipos y docstrings que definamos en cada endpoint.
from fastapi.security import HTTPBearer

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "API REST para el Sistema de Gestión de Turnos Médicos. "
        "Permite administrar hospitales, médicos, pacientes, "
        "disponibilidades y turnos con soporte multi-tenant."
    ),
    version=settings.APP_VERSION,
)


# =============================================================================
# Middleware de CORS (Cross-Origin Resource Sharing)
# =============================================================================
# CORS controla qué dominios externos pueden hacer peticiones a esta API.
#
# Sin esto configurado, el navegador bloquea las peticiones del frontend
# Vue.js hacia el backend FastAPI, aunque estén en la misma máquina
# pero en puertos distintos (ej: :5173 → :8000).
#
# allow_origins: lista de dominios permitidos.
#   - En desarrollo: el servidor Vite de Vue corre en el puerto 5173.
#   - En producción: reemplazar por la URL real del dominio del frontend.
#
# allow_credentials=True: permite enviar cookies y el header Authorization
#   que contiene el token JWT.
#
# allow_methods=["*"]: acepta todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
#
# allow_headers=["*"]: acepta todos los headers, incluyendo Authorization,
#   Content-Type y otros que el frontend pueda necesitar enviar.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Servidor de desarrollo Vite/Vue (puerto por defecto)
        "http://localhost:3000",  # Puerto alternativo
        "http://127.0.0.1:5173", # Misma dirección con IP explícita
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Registro de routers
# =============================================================================
# Cada módulo tiene su propio router con sus endpoints.
# Los vamos descomentando a medida que los creamos.
#
# El prefijo /api/v1/ es una buena práctica que permite versionar la API
# en el futuro sin romper a los clientes existentes
# (ej: cuando saquemos /api/v2/ con cambios incompatibles).
#
# --- DESCOMENTAR A MEDIDA QUE SE CREEN LOS MÓDULOS ---
#
from app.modules.auth.router           import router as auth_router
# from app.modules.hospital.router       import router as hospital_router
# from app.modules.rol.router            import router as rol_router
# from app.modules.especialidad.router   import router as especialidad_router
# from app.modules.obra_social.router    import router as obra_social_router
# from app.modules.dia_semana.router     import router as dia_semana_router
# from app.modules.usuario.router        import router as usuario_router
# from app.modules.medico.router         import router as medico_router
# from app.modules.paciente.router       import router as paciente_router
# from app.modules.disponibilidad.router import router as disponibilidad_router
# from app.modules.turno.router          import router as turno_router
#
# app.include_router(auth_router,            prefix="/api/v1/auth",            tags=["Autenticación"])
app.include_router(auth_router,            prefix="/api/v1/auth",            tags=["Autenticación"])
# app.include_router(hospital_router,        prefix="/api/v1/hospitales",       tags=["Hospitales"])
# app.include_router(rol_router,             prefix="/api/v1/roles",            tags=["Roles"])
# app.include_router(especialidad_router,    prefix="/api/v1/especialidades",   tags=["Especialidades"])
# app.include_router(obra_social_router,     prefix="/api/v1/obras-sociales",   tags=["Obras Sociales"])
# app.include_router(dia_semana_router,      prefix="/api/v1/dias-semana",      tags=["Días de la Semana"])
# app.include_router(usuario_router,         prefix="/api/v1/usuarios",         tags=["Usuarios"])
# app.include_router(medico_router,          prefix="/api/v1/medicos",          tags=["Médicos"])
# app.include_router(paciente_router,        prefix="/api/v1/pacientes",        tags=["Pacientes"])
# app.include_router(disponibilidad_router,  prefix="/api/v1/disponibilidad",   tags=["Disponibilidad"])
# app.include_router(turno_router,           prefix="/api/v1/turnos",           tags=["Turnos"])


# =============================================================================
# Endpoints de verificación (Health Checks)
# =============================================================================

@app.get("/", tags=["Health Check"])
def root():
    """
    Endpoint raíz — confirma que la API está en línea.

    Útil para verificar rápidamente que el servidor arrancó correctamente.
    Retorna información básica del sistema.
    """
    return {
        "sistema":      settings.APP_NAME,
        "version":      settings.APP_VERSION,
        "estado":       "en línea",
        "entorno":      settings.ENVIRONMENT,
        "documentacion": "/docs",
    }


@app.get("/health", tags=["Health Check"])
def health_check():
    """
    Health check estándar para herramientas de monitoreo y deploys.

    Docker, Kubernetes y otras plataformas llaman a este endpoint
    para verificar que la aplicación responde correctamente.
    En el futuro puede incluir verificación de conexión a la BD.
    """
    return {"status": "ok"}