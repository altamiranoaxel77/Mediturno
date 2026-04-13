# =============================================================================
# app/core/jwt.py — Creación y verificación de tokens JWT
# =============================================================================
# Responsabilidad: generar tokens JWT al hacer login y verificarlos
# en cada petición protegida.
#
# ¿Cómo funciona JWT?
# 1. El usuario hace login con email + password
# 2. Si las credenciales son correctas, el servidor genera un token JWT
# 3. El token contiene datos del usuario (payload) firmados con SECRET_KEY
# 4. El frontend guarda el token y lo envía en cada petición:
#    Header → Authorization: Bearer <token>
# 5. El servidor verifica la firma del token y extrae los datos del usuario
#
# El token tiene 3 partes separadas por puntos:
#   header.payload.signature
#   - header: algoritmo usado
#   - payload: datos del usuario (visible pero no modificable sin la clave)
#   - signature: garantiza que el token no fue alterado
# =============================================================================

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt                     # python-jose para JWT
from app.config import settings                    # SECRET_KEY, ALGORITHM, etc.
from app.modules.auth.schema import TokenData      # Schema del payload del token


def crear_token(data: dict) -> str:
    """
    Genera un token JWT firmado con los datos del usuario.

    Parámetros:
        data: diccionario con los datos a incluir en el payload del token.
                Debe contener al menos: sub, id_usuario, id_hospital, id_rol

    Retorna:
        String con el token JWT listo para enviar al frontend.

    Ejemplo de uso en AuthService:
        token = crear_token({
            "sub":         usuario.email,
            "id_usuario":  usuario.id_usuario,
            "id_hospital": usuario.id_hospital,
            "id_rol":      usuario.id_rol,
        })
    """
    # Copiamos el dict para no modificar el original
    payload = data.copy()

    # Calculamos la fecha de expiración del token
    # timezone.utc garantiza que trabajamos siempre en UTC — evita bugs de zona horaria
    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # "exp" es un campo estándar de JWT — python-jose lo valida automáticamente
    payload.update({"exp": expiracion})

    # Firmamos el token con la SECRET_KEY usando el algoritmo configurado (HS256)
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return token


def verificar_token(token: str) -> TokenData:
    """
    Verifica y decodifica un token JWT.

    Parámetros:
        token: el string JWT enviado por el frontend en el header Authorization

    Retorna:
        TokenData con los datos del usuario extraídos del payload

    Lanza:
        JWTError si el token es inválido, expiró o fue manipulado.
        Esta excepción se captura en dependencies.py y se convierte
        en una respuesta HTTP 401 Unauthorized.

    El proceso de verificación incluye:
        1. Verificar la firma con SECRET_KEY (garantiza que lo generamos nosotros)
        2. Verificar que no haya expirado (campo "exp")
        3. Extraer el payload con los datos del usuario
    """
    # Decodificamos y verificamos el token en un solo paso
    # Si el token es inválido o expiró, jwt.decode lanza JWTError automáticamente
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )

    # Extraemos los datos del payload y los mapeamos al schema TokenData
    return TokenData(
        sub=        payload.get("sub"),
        id_usuario= payload.get("id_usuario"),
        id_hospital=payload.get("id_hospital"),
        id_rol=     payload.get("id_rol"),
    )