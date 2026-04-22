# =============================================================================
# modules/usuario/router.py — Endpoints HTTP para Usuario
# =============================================================================

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import require_roles, get_current_user
from app.core.roles import Roles
from app.modules.usuario.schema import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.modules.usuario.service import usuario_service
from app.modules.usuario.model import Usuario

router = APIRouter()


@router.get(
    "/",
    response_model=list[UsuarioResponse],
    summary="Listar usuarios del hospital",
    description="Retorna todos los usuarios activos del hospital del usuario autenticado."
)
def listar_usuarios(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(Roles.SUPERADMIN, Roles.ADMIN))
):
    # El Admin lista los usuarios de su propio hospital
    # El SuperAdmin necesita pasar id_hospital como query param (pendiente)
    return usuario_service.listar(db, current_user.id_hospital)


@router.get(
    "/{id_usuario}",
    response_model=UsuarioResponse,
    summary="Obtener usuario por ID"
)
def obtener_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(Roles.SUPERADMIN, Roles.ADMIN))
):
    return usuario_service.obtener_por_id(db, id_usuario)


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description=(
        "Crea un nuevo usuario. "
        "SuperAdmin puede crear Admins asignados a cualquier hospital. "
        "Admin puede crear Secretarios y Doctores solo en su propio hospital."
    )
)
def crear_usuario(
    datos: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(Roles.SUPERADMIN, Roles.ADMIN))
):
    return usuario_service.crear(
        db=db,
        datos=datos,
        rol_creador=current_user.rol.nombre,
        id_hospital_creador=current_user.id_hospital
    )


@router.put(
    "/{id_usuario}",
    response_model=UsuarioResponse,
    summary="Actualizar usuario"
)
def actualizar_usuario(
    id_usuario: int,
    datos: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(Roles.SUPERADMIN, Roles.ADMIN))
):
    return usuario_service.actualizar(
        db=db,
        id_usuario=id_usuario,
        datos=datos,
        rol_creador=current_user.rol.nombre,
        id_hospital_creador=current_user.id_hospital
    )


@router.put(
    "/{id_usuario}/desactivar",
    response_model=UsuarioResponse,
    summary="Desactivar usuario",
    description="Baja lógica del usuario — cambia activo a False. No elimina el registro."
)
def desactivar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(Roles.SUPERADMIN, Roles.ADMIN))
):
    return usuario_service.desactivar(
        db=db,
        id_usuario=id_usuario,
        rol_creador=current_user.rol.nombre,
        id_hospital_creador=current_user.id_hospital
    )