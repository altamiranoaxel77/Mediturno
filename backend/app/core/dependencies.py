# =============================================================================
# app/core/dependencies.py — Dependencias de autenticación y autorización
# =============================================================================
# Responsabilidad: proveer funciones que FastAPI inyecta en los endpoints
# para verificar que el usuario esté autenticado y tenga el rol correcto.
#
# Hay dos niveles de protección:
#
#   1. get_current_user → verifica que el token JWT sea válido.
#                         Si no hay token o es inválido → 401 Unauthorized
#
#   2. require_roles()  → verifica que el usuario tenga uno de los roles
#                         permitidos para ese endpoint.
#                         Si el rol no coincide → 403 Forbidden
#
# Uso en los routers:
#   # Solo requiere estar logueado
#   @router.get("/algo")
#   def endpoint(current_user = Depends(get_current_user)):
#
#   # Requiere rol específico
#   @router.post("/turnos")
#   def crear_turno(current_user = Depends(require_roles(Roles.SECRETARIO, Roles.ADMIN))):
# =============================================================================

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer  # Extrae el token del header Authorization
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.jwt import verificar_token
from app.core.roles import Roles
from app.modules.usuario.model import Usuario
from app.modules.auth.schema import TokenData


# OAuth2PasswordBearer indica a FastAPI dónde está el endpoint de login
# y cómo extraer el token del header Authorization: Bearer <token>
# tokenUrl es solo informativo para Swagger UI — no afecta la lógica
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependencia que verifica el token JWT y retorna el usuario autenticado.

    Proceso:
        1. FastAPI extrae el token del header Authorization: Bearer <token>
        2. Verificamos y decodificamos el token con verificar_token()
        3. Buscamos el usuario en la BD por su id_usuario del payload
        4. Verificamos que el usuario esté activo (baja lógica)
        5. Retornamos el objeto Usuario para que el endpoint lo use

    Si algo falla en cualquier paso → HTTP 401 Unauthorized
    """
    # Excepción reutilizable para cualquier fallo de autenticación
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales.",
        # WWW-Authenticate es el header estándar para indicar que se necesita Bearer token
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Verificar y decodificar el token — lanza JWTError si es inválido o expiró
        token_data: TokenData = verificar_token(token)

        # El token debe tener id_usuario en el payload
        if token_data.id_usuario is None:
            raise credenciales_invalidas

    except JWTError:
        # Token inválido, manipulado o expirado
        raise credenciales_invalidas

    # Buscar el usuario en la base de datos
    usuario = db.query(Usuario).filter(
        Usuario.id_usuario == token_data.id_usuario
    ).first()

    # Si el usuario no existe en la BD
    if usuario is None:
        raise credenciales_invalidas

    # Si el usuario fue dado de baja lógicamente
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo. Contacte al administrador.",
        )

    return usuario


def require_roles(*roles_permitidos: str):
    """
    Fábrica de dependencias que verifica que el usuario tenga
    uno de los roles permitidos para acceder al endpoint.

    Parámetros:
        *roles_permitidos: uno o más nombres de roles que pueden acceder.
                            Usar las constantes de app.core.roles.Roles

    Retorna:
        Una función de dependencia lista para usar con Depends()

    Ejemplos:
        # Solo SuperAdmin puede crear hospitales
        Depends(require_roles(Roles.SUPERADMIN))

        # Admin y Secretario pueden gestionar turnos
        Depends(require_roles(Roles.ADMIN, Roles.SECRETARIO))

    Si el rol del usuario no está en la lista → HTTP 403 Forbidden
    """
    def verificar_rol(
        current_user: Usuario = Depends(get_current_user)
    ) -> Usuario:
        """
        Verifica que el rol del usuario esté en la lista de roles permitidos.
        current_user ya viene verificado por get_current_user.
        """
        # Accedemos al nombre del rol a través de la relación ORM
        # current_user.rol es el objeto Rol cargado con lazy="joined"
        rol_usuario = current_user.rol.nombre

        if rol_usuario not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Acceso denegado. "
                    f"Se requiere uno de los siguientes roles: {', '.join(roles_permitidos)}. "
                    f"Tu rol actual es: {rol_usuario}."
                ),
            )

        return current_user

    return verificar_rol


def get_current_hospital_id(
    current_user: Usuario = Depends(get_current_user)
) -> int:
    """
    Dependencia auxiliar que retorna el id_hospital del usuario autenticado.

    Se usa en endpoints multi-tenant para filtrar automáticamente
    los datos por hospital sin que el frontend tenga que enviarlo.

    Ejemplo de uso:
        @router.get("/pacientes")
        def listar_pacientes(
            id_hospital: int = Depends(get_current_hospital_id),
            db: Session = Depends(get_db)
        ):
            return paciente_service.listar(db, id_hospital)
    """
    return current_user.id_hospital