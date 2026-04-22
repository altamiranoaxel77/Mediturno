from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
import app.models  # noqa: F401

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "API REST para el Sistema de Gestión de Turnos Médicos. "
        "Permite administrar hospitales, médicos, pacientes, "
        "disponibilidades y turnos con soporte multi-tenant."
    ),
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────────────────
from app.modules.auth.router           import router as auth_router
from app.modules.hospital.router       import router as hospital_router
from app.modules.usuario.router        import router as usuario_router
from app.modules.rol.router            import router as rol_router
from app.modules.especialidad.router   import router as especialidad_router
from app.modules.obra_social.router    import router as obra_social_router
from app.modules.medico.router         import router as medico_router
from app.modules.paciente.router       import router as paciente_router
# from app.modules.dia_semana.router   import router as dia_semana_router
# from app.modules.disponibilidad.router import router as disponibilidad_router
# from app.modules.turno.router          import router as turno_router

app.include_router(auth_router,         prefix="/api/v1/auth",          tags=["Autenticación"])
app.include_router(hospital_router,     prefix="/api/v1/hospitales",     tags=["Hospitales"])
app.include_router(usuario_router,      prefix="/api/v1/usuarios",       tags=["Usuarios"])
app.include_router(rol_router,          prefix="/api/v1/roles",          tags=["Roles"])
app.include_router(especialidad_router, prefix="/api/v1/especialidades", tags=["Especialidades"])
app.include_router(obra_social_router,  prefix="/api/v1/obras-sociales", tags=["Obras Sociales"])
app.include_router(medico_router,       prefix="/api/v1/medicos",        tags=["Médicos"])
app.include_router(paciente_router,     prefix="/api/v1/pacientes",      tags=["Pacientes"])
# app.include_router(dia_semana_router,      prefix="/api/v1/dias-semana",      tags=["Días"])
# app.include_router(disponibilidad_router,  prefix="/api/v1/disponibilidad",   tags=["Disponibilidad"])
# app.include_router(turno_router,           prefix="/api/v1/turnos",           tags=["Turnos"])

# ── Health Checks ──────────────────────────────────────────────────────────────
@app.get("/", tags=["Health Check"])
def root():
    return {
        "sistema":       settings.APP_NAME,
        "version":       settings.APP_VERSION,
        "estado":        "en línea",
        "entorno":       settings.ENVIRONMENT,
        "documentacion": "/docs",
    }

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok"}