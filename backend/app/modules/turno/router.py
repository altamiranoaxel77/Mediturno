# =============================================================================
# modules/turno/router.py
# =============================================================================

from datetime import date
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import require_roles, get_current_user
from app.core.roles import Roles
from app.modules.turno.schema import (
    TurnoCreate, TurnoUpdate, TurnoActualizarEstado,
    TurnoResponse, SlotDisponible
)
from app.modules.turno.service import turno_service
from app.modules.usuario.model import Usuario

router = APIRouter()


# =============================================================================
# Slots disponibles — el endpoint más importante del sistema
# =============================================================================

@router.get(
    "/disponibles",
    response_model=list[SlotDisponible],
    summary="Consultar horarios disponibles",
    description=(
        "Retorna los slots horarios libres de un médico para una fecha. "
        "Excluye automáticamente los horarios ya ocupados por otros turnos. "
        "El frontend usa estos slots para mostrar los botones de horarios disponibles."
    )
)
def obtener_slots_disponibles(
    id_medico: int  = Query(..., description="ID del médico"),
    fecha:     date = Query(..., description="Fecha en formato YYYY-MM-DD"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(Roles.ADMIN, Roles.SECRETARIO)
    )
):
    return turno_service.obtener_slots_disponibles(
        db, id_medico, fecha, current_user.id_hospital
    )


# =============================================================================
# Agenda del médico — para el Doctor y el Secretario
# =============================================================================

@router.get(
    "/agenda",
    response_model=list[TurnoResponse],
    summary="Ver agenda del día",
    description=(
        "Retorna los turnos de un médico para una fecha. "
        "El Doctor solo puede ver su propia agenda. "
        "Admin y Secretario pueden ver la de cualquier médico del hospital."
    )
)
def obtener_agenda(
    id_medico: int  = Query(..., description="ID del médico"),
    fecha:     date = Query(..., description="Fecha en formato YYYY-MM-DD"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    # Si es Doctor, solo puede ver su propia agenda
    if current_user.rol.nombre == Roles.DOCTOR:
        # Verificar que el médico solicitado sea el mismo que está logueado
        if not current_user.medico or current_user.medico.id_medico != id_medico:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo podés consultar tu propia agenda."
            )

    return turno_service.obtener_agenda_medico(
        db, id_medico, fecha, current_user.id_hospital
    )


# =============================================================================
# Historial de turnos de un paciente
# =============================================================================

@router.get(
    "/paciente/{id_paciente}",
    response_model=list[TurnoResponse],
    summary="Historial de turnos de un paciente"
)
def obtener_turnos_paciente(
    id_paciente: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(Roles.ADMIN, Roles.SECRETARIO)
    )
):
    return turno_service.obtener_por_paciente(
        db, id_paciente, current_user.id_hospital
    )


# =============================================================================
# Obtener un turno por ID
# =============================================================================

@router.get(
    "/{id_turno}",
    response_model=TurnoResponse,
    summary="Obtener turno por ID"
)
def obtener_turno(
    id_turno: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles(Roles.ADMIN, Roles.SECRETARIO, Roles.DOCTOR))
):
    return turno_service.obtener_por_id(db, id_turno)


# =============================================================================
# Registrar turno
# =============================================================================

@router.post(
    "/",
    response_model=TurnoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar turno",
    description=(
        "Registra un nuevo turno para un paciente. "
        "Valida disponibilidad del médico, que el horario esté libre "
        "y que no haya superposición con otros turnos."
    )
)
def crear_turno(
    datos: TurnoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(Roles.ADMIN, Roles.SECRETARIO)
    )
):
    return turno_service.crear(db, datos, current_user.id_hospital)


# =============================================================================
# Actualizar estado del turno
# =============================================================================

@router.put(
    "/{id_turno}/estado",
    response_model=TurnoResponse,
    summary="Actualizar estado del turno",
    description=(
        "Cambia el estado de un turno. "
        "Estados válidos: pendiente → atendido | cancelado | ausente. "
        "No se puede modificar un turno ya atendido o cancelado."
    )
)
def actualizar_estado_turno(
    id_turno: int,
    datos: TurnoActualizarEstado,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(Roles.ADMIN, Roles.SECRETARIO, Roles.DOCTOR)
    )
):
    return turno_service.actualizar_estado(
        db, id_turno, datos, current_user.id_hospital
    )


# =============================================================================
# Actualizar datos del turno (motivo, observaciones)
# =============================================================================

@router.put(
    "/{id_turno}",
    response_model=TurnoResponse,
    summary="Actualizar datos del turno"
)
def actualizar_turno(
    id_turno: int,
    datos: TurnoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(Roles.ADMIN, Roles.SECRETARIO, Roles.DOCTOR)
    )
):
    return turno_service.actualizar_datos(
        db, id_turno, datos, current_user.id_hospital
    )