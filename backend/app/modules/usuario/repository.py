# =============================================================================
# modules/usuario/repository.py — Acceso a datos para Usuario
# =============================================================================

from sqlalchemy.orm import Session
from app.modules.usuario.model import Usuario


class UsuarioRepository:

    def obtener_todos(self, db: Session, id_hospital: int) -> list[Usuario]:
        """
        Retorna todos los usuarios activos de un hospital específico.
        El SuperAdmin no se lista aquí — pertenece a la plataforma, no a un hospital.
        """
        return db.query(Usuario).filter(
            Usuario.id_hospital == id_hospital,
            Usuario.activo == True
        ).all()

    def obtener_por_id(self, db: Session, id_usuario: int) -> Usuario | None:
        """Busca un usuario por su ID sin importar el estado."""
        return db.query(Usuario).filter(
            Usuario.id_usuario == id_usuario
        ).first()

    def obtener_por_email(self, db: Session, email: str) -> Usuario | None:
        """
        Busca un usuario por email incluyendo inactivos.
        Se usa para validar duplicados al crear o modificar.
        """
        return db.query(Usuario).filter(
            Usuario.email == email
        ).first()

    def obtener_por_dni(self, db: Session, dni: str) -> Usuario | None:
        """
        Busca un usuario por DNI incluyendo inactivos.
        Se usa para validar duplicados al crear o modificar.
        """
        return db.query(Usuario).filter(
            Usuario.dni == dni
        ).first()

    def crear(self, db: Session, usuario: Usuario) -> Usuario:
        """Persiste un nuevo usuario en la base de datos."""
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    def actualizar(self, db: Session, usuario: Usuario) -> Usuario:
        """Guarda los cambios de un usuario ya modificado por el service."""
        db.commit()
        db.refresh(usuario)
        return usuario

    def desactivar(self, db: Session, usuario: Usuario) -> Usuario:
        """
        Baja lógica — marca el usuario como inactivo.
        No elimina el registro para mantener la integridad histórica.
        """
        usuario.activo = False
        db.commit()
        db.refresh(usuario)
        return usuario