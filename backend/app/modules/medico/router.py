# =============================================================================
# modules/medico/router.py
# =============================================================================

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import require_roles
from app.core.roles import Roles
from app.modules.medico.schema import MedicoCreate, MedicoUpdate, MedicoResponse
from app.modules.medico.service import medico_service
from app.modules.usuario.model import Usuario

router = APIRouter()

# Admin y Secretario pueden consultar médicos
# Solo Admin puede crear, modificar y desactivar
admin_secretario = Depends(require_roles(Roles.ADMIN, Roles.SECRETARIO))
solo_admin = Depends(require_roles(Roles.ADMIN))


@router.get(
    "/",
    response_model=list[MedicoResponse],
    summary="Listar médicos del hospital"
)
def listar_medicos(
    id_especialidad: int | None = Query(None, description="Filtrar por especialidad"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(Roles.ADMIN, Roles.SECRETARIO))
):
    if id_especialidad:
        return medico_service.listar_por_especialidad(db, id_especialidad, current_user.id_hospital)
    return medico_service.listar(db, current_user.id_hospital)


@router.get("/{id_medico}", response_model=MedicoResponse, summary="Obtener médico por ID")
def obtener_medico(
    id_medico: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles(Roles.ADMIN, Roles.SECRETARIO))
):
    return medico_service.obtener_por_id(db, id_medico)


@router.post(
    "/",
    response_model=MedicoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar médico",
    description=(
        "Asocia un usuario existente como médico del hospital. "
        "El usuario debe tener rol Doctor y pertenecer al mismo hospital."
    )
)
def crear_medico(
    datos: MedicoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(Roles.ADMIN))
):
    return medico_service.crear(db, datos, current_user.id_hospital)


@router.put("/{id_medico}", response_model=MedicoResponse, summary="Modificar médico")
def actualizar_medico(
    id_medico: int,
    datos: MedicoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(Roles.ADMIN))
):
    return medico_service.actualizar(db, id_medico, datos, current_user.id_hospital)


@router.put(
    "/{id_medico}/desactivar",
    response_model=MedicoResponse,
    summary="Desactivar médico",
    description="Baja lógica del médico. No elimina sus turnos ni disponibilidades históricas."
)
def desactivar_medico(
    id_medico: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(Roles.ADMIN))
):
    return medico_service.desactivar(db, id_medico, current_user.id_hospital)