# =============================================================================
# app/core/dependencies.py — Dependencias de autenticación y autorización
# =============================================================================

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.jwt import verificar_token
from app.core.roles import Roles
from app.modules.usuario.model import Usuario
from app.modules.auth.schema import TokenData

# HTTPBearer extrae el token del header Authorization: Bearer <token>
# Swagger UI mostrará un campo de texto simple para pegar el token directamente
# auto_error=False permite manejar el error manualmente con mensajes descriptivos
oauth2_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
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
    """
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Si no se envió ningún token en el header
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere autenticación. Incluí el token en el header Authorization: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # credentials.credentials contiene solo el token, sin la palabra "Bearer"
        token = credentials.credentials

        # Verificar y decodificar el token
        token_data: TokenData = verificar_token(token)

        if token_data.id_usuario is None:
            raise credenciales_invalidas

    except JWTError:
        raise credenciales_invalidas

    # Buscar el usuario en la base de datos
    usuario = db.query(Usuario).filter(
        Usuario.id_usuario == token_data.id_usuario
    ).first()

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

    Ejemplos:
        # Solo SuperAdmin puede crear hospitales
        Depends(require_roles(Roles.SUPERADMIN))

        # Admin y Secretario pueden gestionar turnos
        Depends(require_roles(Roles.ADMIN, Roles.SECRETARIO))
    """
    def verificar_rol(
        current_user: Usuario = Depends(get_current_user)
    ) -> Usuario:
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
    Retorna el id_hospital del usuario autenticado.
    Se usa en endpoints multi-tenant para filtrar datos por hospital
    sin que el frontend tenga que enviarlo explícitamente.
    """
    return current_user.id_hospital