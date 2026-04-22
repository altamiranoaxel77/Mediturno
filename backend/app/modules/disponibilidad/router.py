# =============================================================================
# modules/disponibilidad/router.py
# =============================================================================

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import require_roles
from app.core.roles import Roles
from app.modules.disponibilidad.schema import (
    DisponibilidadCreate, DisponibilidadUpdate, DisponibilidadResponse
)
from app.modules.disponibilidad.service import disponibilidad_service
from app.modules.usuario.model import Usuario

router = APIRouter()


@router.get(
    "/medico/{id_medico}",
    response_model=list[DisponibilidadResponse],
    summary="Ver agenda semanal de un médico",
    description="Retorna todos los días y horarios configurados para el médico."
)
def listar_disponibilidad_medico(
    id_medico: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(Roles.ADMIN, Roles.SECRETARIO)
    )
):
    return disponibilidad_service.listar_por_medico(
        db, id_medico, current_user.id_hospital
    )


@router.get(
    "/{id_disponibilidad}",
    response_model=DisponibilidadResponse,
    summary="Obtener disponibilidad por ID"
)
def obtener_disponibilidad(
    id_disponibilidad: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles(Roles.ADMIN, Roles.SECRETARIO))
):
    return disponibilidad_service.obtener_por_id(db, id_disponibilidad)


@router.post(
    "/",
    response_model=DisponibilidadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Configurar disponibilidad de un médico",
    description=(
        "Define los días y horarios de atención de un médico. "
        "Se puede configurar turno mañana, tarde o ambos por día. "
        "Admin y Secretario pueden gestionar disponibilidades."
    )
)
def crear_disponibilidad(
    datos: DisponibilidadCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(Roles.ADMIN, Roles.SECRETARIO)
    )
):
    return disponibilidad_service.crear(db, datos, current_user.id_hospital)


@router.put(
    "/{id_disponibilidad}",
    response_model=DisponibilidadResponse,
    summary="Modificar disponibilidad",
    description="Actualiza los horarios de un día ya configurado."
)
def actualizar_disponibilidad(
    id_disponibilidad: int,
    datos: DisponibilidadUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(Roles.ADMIN, Roles.SECRETARIO)
    )
):
    return disponibilidad_service.actualizar(
        db, id_disponibilidad, datos, current_user.id_hospital
    )


@router.put(
    "/{id_disponibilidad}/desactivar",
    response_model=DisponibilidadResponse,
    summary="Desactivar disponibilidad",
    description=(
        "Baja lógica — el médico deja de atender ese día. "
        "No cancela los turnos futuros automáticamente."
    )
)
def desactivar_disponibilidad(
    id_disponibilidad: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(Roles.ADMIN, Roles.SECRETARIO)
    )
):
    return disponibilidad_service.desactivar(
        db, id_disponibilidad, current_user.id_hospital
    )