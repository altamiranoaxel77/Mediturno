# =============================================================================
# modules/especialidad/router.py
# =============================================================================

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import require_roles
from app.core.roles import Roles
from app.modules.especialidad.schema import EspecialidadCreate, EspecialidadUpdate, EspecialidadResponse
from app.modules.especialidad.service import especialidad_service

router = APIRouter()

# Las especialidades las gestiona solo el SuperAdmin — son globales al sistema
solo_superadmin = Depends(require_roles(Roles.SUPERADMIN))


@router.get("/", response_model=list[EspecialidadResponse], summary="Listar especialidades")
def listar_especialidades(db: Session = Depends(get_db)):
    # GET público — cualquier usuario autenticado puede ver las especialidades
    # para asignarlas a médicos
    return especialidad_service.listar(db)


@router.get("/{id_especialidad}", response_model=EspecialidadResponse)
def obtener_especialidad(id_especialidad: int, db: Session = Depends(get_db)):
    return especialidad_service.obtener_por_id(db, id_especialidad)


@router.post("/", response_model=EspecialidadResponse, status_code=status.HTTP_201_CREATED,
            summary="Crear especialidad")
def crear_especialidad(
    datos: EspecialidadCreate,
    db: Session = Depends(get_db),
    _: None = solo_superadmin
):
    return especialidad_service.crear(db, datos)


@router.put("/{id_especialidad}", response_model=EspecialidadResponse, summary="Actualizar especialidad")
def actualizar_especialidad(
    id_especialidad: int,
    datos: EspecialidadUpdate,
    db: Session = Depends(get_db),
    _: None = solo_superadmin
):
    return especialidad_service.actualizar(db, id_especialidad, datos)


@router.put("/{id_especialidad}/desactivar", response_model=EspecialidadResponse,
            summary="Desactivar especialidad")
def desactivar_especialidad(
    id_especialidad: int,
    db: Session = Depends(get_db),
    _: None = solo_superadmin
):
    return especialidad_service.desactivar(db, id_especialidad)