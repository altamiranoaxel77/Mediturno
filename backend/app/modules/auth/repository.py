# =============================================================================
# modules/auth/repository.py — Acceso a datos para autenticación
# =============================================================================
# Responsabilidad: SOLO consultas a la base de datos relacionadas con auth.
# No contiene lógica de negocio — eso va en el service.
# =============================================================================

from sqlalchemy.orm import Session
from app.modules.usuario.model import Usuario


class AuthRepository:

    def obtener_usuario_por_email(self, db: Session, email: str) -> Usuario | None:
        """
        Busca un usuario por su email incluyendo usuarios inactivos.
        El service decide qué hacer si el usuario está inactivo.

        Retorna el objeto Usuario o None si no existe.
        """
        return db.query(Usuario).filter(
            Usuario.email == email
        ).first()