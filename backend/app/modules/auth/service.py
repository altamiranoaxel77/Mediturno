# =============================================================================
# modules/auth/service.py — Lógica de negocio para autenticación
# =============================================================================
# Responsabilidad: validar credenciales y generar el token JWT.
# Toda la lógica de negocio del login vive aquí — no en el router.
# =============================================================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.security import verificar_password
from app.core.jwt import crear_token
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schema import LoginRequest, TokenResponse


class AuthService:

    def __init__(self):
        # Instanciamos el repository — el service lo usa para acceder a la BD
        self.repository = AuthRepository()

    def login(self, db: Session, datos: LoginRequest) -> TokenResponse:
        """
        Valida las credenciales del usuario y retorna un token JWT.

        Proceso:
            1. Buscar el usuario por email
            2. Verificar que exista y esté activo
            3. Verificar que la contraseña sea correcta
            4. Generar y retornar el token JWT

        Seguridad importante:
            Siempre retornamos el mismo mensaje de error genérico
            tanto si el email no existe como si la contraseña es incorrecta.
            Esto evita que un atacante pueda saber qué emails están registrados
            en el sistema (enumeración de usuarios).
        """
        # Mensaje genérico — no revelamos si el email existe o no
        error_credenciales = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

        # 1. Buscar usuario por email
        usuario = self.repository.obtener_usuario_por_email(db, datos.email)

        # 2. Si no existe → error genérico (no revelamos que el email no existe)
        if not usuario:
            raise error_credenciales

        # 3. Si está inactivo → error específico (ya sabe que tiene cuenta)
        if not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario inactivo. Contacte al administrador.",
            )

        # 4. Verificar contraseña — compara el texto plano contra el hash de la BD
        if not verificar_password(datos.password, usuario.password):
            raise error_credenciales

        # 5. Generar token JWT con los datos necesarios para el sistema multi-tenant
        token = crear_token({
            "sub":         usuario.email,       # identificador estándar JWT
            "id_usuario":  usuario.id_usuario,
            "id_hospital": usuario.id_hospital, # clave para el filtro multi-tenant
            "id_rol":      usuario.id_rol,      # necesario para control de acceso
        })

        return TokenResponse(access_token=token)


# Instancia única del service — se importa desde el router
auth_service = AuthService()