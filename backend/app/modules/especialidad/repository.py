# =============================================================================
# modules/especialidad/repository.py
# =============================================================================

from sqlalchemy.orm import Session
from app.modules.especialidad.model import Especialidad


class EspecialidadRepository:

    def obtener_todas(self, db: Session) -> list[Especialidad]:
        """Retorna todas las especialidades activas."""
        return db.query(Especialidad).filter(
            Especialidad.activo == True
        ).all()

    def obtener_por_id(self, db: Session, id_especialidad: int) -> Especialidad | None:
        return db.query(Especialidad).filter(
            Especialidad.id_especialidad == id_especialidad,
            Especialidad.activo == True
        ).first()

    def obtener_por_nombre(self, db: Session, nombre: str) -> Especialidad | None:
        """Búsqueda case-insensitive para validar duplicados."""
        return db.query(Especialidad).filter(
            Especialidad.nombre.ilike(nombre)
        ).first()

    def crear(self, db: Session, especialidad: Especialidad) -> Especialidad:
        db.add(especialidad)
        db.commit()
        db.refresh(especialidad)
        return especialidad

    def actualizar(self, db: Session, especialidad: Especialidad) -> Especialidad:
        db.commit()
        db.refresh(especialidad)
        return especialidad

    def desactivar(self, db: Session, especialidad: Especialidad) -> Especialidad:
        especialidad.activo = False
        db.commit()
        db.refresh(especialidad)
        return especialidad