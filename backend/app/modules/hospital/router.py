# =============================================================================
# modules/hospital/router.py — Endpoints HTTP para Hospital
# =============================================================================
# Solo el SuperAdmin puede acceder a estos endpoints.
# Los demás roles trabajan siempre dentro de su propio hospital.
# =============================================================================

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import require_roles
from app.core.roles import Roles
from app.modules.hospital.schema import HospitalCreate, HospitalUpdate, HospitalResponse
from app.modules.hospital.service import hospital_service

router = APIRouter()

# Dependencia reutilizable — todos los endpoints de este router
# requieren rol SuperAdmin
solo_superadmin = Depends(require_roles(Roles.SUPERADMIN))


@router.get(
    "/",
    response_model=list[HospitalResponse],
    summary="Listar todos los hospitales",
    description="Retorna todos los hospitales activos del sistema. Solo SuperAdmin."
)
def listar_hospitales(
    db: Session = Depends(get_db),
    _: None = solo_superadmin
):
    return hospital_service.listar(db)


@router.get(
    "/{id_hospital}",
    response_model=HospitalResponse,
    summary="Obtener hospital por ID",
)
def obtener_hospital(
    id_hospital: int,
    db: Session = Depends(get_db),
    _: None = solo_superadmin
):
    return hospital_service.obtener_por_id(db, id_hospital)


@router.post(
    "/",
    response_model=HospitalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear hospital",
    description="Crea un nuevo hospital en el sistema. Solo SuperAdmin."
)
def crear_hospital(
    datos: HospitalCreate,
    db: Session = Depends(get_db),
    _: None = solo_superadmin
):
    return hospital_service.crear(db, datos)


@router.put(
    "/{id_hospital}",
    response_model=HospitalResponse,
    summary="Actualizar hospital",
    description="Modifica los datos de un hospital existente. Solo SuperAdmin."
)
def actualizar_hospital(
    id_hospital: int,
    datos: HospitalUpdate,
    db: Session = Depends(get_db),
    _: None = solo_superadmin
):
    return hospital_service.actualizar(db, id_hospital, datos)


@router.put(
    "/{id_hospital}/desactivar",
    response_model=HospitalResponse,
    summary="Desactivar hospital",
    description=(
        "Baja lógica del hospital — cambia activo a False. "
        "No elimina el registro ni sus datos históricos. Solo SuperAdmin."
    )
)
def desactivar_hospital(
    id_hospital: int,
    db: Session = Depends(get_db),
    _: None = solo_superadmin
):
    return hospital_service.desactivar(db, id_hospital)