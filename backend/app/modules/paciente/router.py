# =============================================================================
# modules/paciente/router.py
# =============================================================================

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import require_roles
from app.core.roles import Roles
from app.modules.paciente.schema import PacienteCreate, PacienteUpdate, PacienteResponse
from app.modules.paciente.service import paciente_service
from app.modules.usuario.model import Usuario

router = APIRouter()


@router.get("/", response_model=list[PacienteResponse], summary="Listar pacientes del hospital")
def listar_pacientes(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(Roles.ADMIN, Roles.SECRETARIO))
):
    return paciente_service.listar(db, current_user.id_hospital)


@router.get("/buscar", response_model=PacienteResponse, summary="Buscar paciente por DNI")
def buscar_por_dni(
    dni: str = Query(..., description="DNI del paciente"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(Roles.ADMIN, Roles.SECRETARIO))
):
    # Endpoint clave para el registro de turnos — el secretario busca al paciente por DNI
    return paciente_service.obtener_por_dni(db, dni, current_user.id_hospital)


@router.get("/{id_paciente}", response_model=PacienteResponse, summary="Obtener paciente por ID")
def obtener_paciente(
    id_paciente: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles(Roles.ADMIN, Roles.SECRETARIO))
):
    return paciente_service.obtener_por_id(db, id_paciente)


@router.post(
    "/",
    response_model=PacienteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar paciente"
)
def crear_paciente(
    datos: PacienteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(Roles.ADMIN, Roles.SECRETARIO))
):
    return paciente_service.crear(db, datos, current_user.id_hospital)


@router.put("/{id_paciente}", response_model=PacienteResponse, summary="Modificar paciente")
def actualizar_paciente(
    id_paciente: int,
    datos: PacienteUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(Roles.ADMIN, Roles.SECRETARIO))
):
    return paciente_service.actualizar(db, id_paciente, datos, current_user.id_hospital)


@router.put("/{id_paciente}/desactivar", response_model=PacienteResponse, summary="Desactivar paciente")
def desactivar_paciente(
    id_paciente: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(Roles.ADMIN, Roles.SECRETARIO))
):
    return paciente_service.desactivar(db, id_paciente, current_user.id_hospital)