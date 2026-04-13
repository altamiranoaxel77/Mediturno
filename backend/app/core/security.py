# =============================================================================
# app/core/security.py — Manejo seguro de contraseñas
# =============================================================================
# Responsabilidad: hashear contraseñas al crear usuarios y verificarlas
# al hacer login. Usa bcrypt a través de passlib.
#
# ¿Por qué bcrypt?
# - Es un algoritmo diseñado específicamente para contraseñas
# - Es lento a propósito — dificulta los ataques de fuerza bruta
# - Incluye un "salt" automático — dos passwords iguales generan hashes distintos
# - Es el estándar de la industria para almacenamiento de contraseñas
#
# REGLA: la contraseña en texto plano NUNCA se guarda en la base de datos.
#        Solo se guarda el hash que genera esta función.
# =============================================================================

from passlib.context import CryptContext

# CryptContext configura el algoritmo de hashing.
# schemes=["bcrypt"] → usamos bcrypt como algoritmo principal
# deprecated="auto"  → si en el futuro cambiamos de algoritmo, los hashes
#                       viejos se marcan como deprecados automáticamente
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashear_password(password: str) -> str:
    """
    Convierte una contraseña en texto plano a un hash seguro de bcrypt.

    Ejemplo:
        hashear_password("mipassword123")
        → "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"

    El hash resultante tiene siempre 60 caracteres y es único cada vez
    aunque se llame con la misma contraseña (por el salt interno de bcrypt).

    Se usa en: UsuarioService.crear() antes de guardar en la BD
    """
    return pwd_context.hash(password)


def verificar_password(password_plano: str, password_hash: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su hash almacenado.

    Ejemplo:
        verificar_password("mipassword123", hash_de_la_bd)
        → True si la contraseña es correcta, False si no

    Se usa en: AuthService.login() al verificar las credenciales del usuario
    """
    return pwd_context.verify(password_plano, password_hash)