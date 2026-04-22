# =============================================================================
# modules/medico/repository.py
# =============================================================================

from sqlalchemy.orm import Session
from app.modules.medico.model import Medico


class MedicoRepository:

    def obtener_todos(self, db: Session, id_hospital: int) -> list[Medico]:
        """Retorna todos los médicos activos de un hospital — multi-tenant."""
        return db.query(Medico).filter(
            Medico.id_hospital == id_hospital,
            Medico.activo == True
        ).all()

    def obtener_por_id(self, db: Session, id_medico: int) -> Medico | None:
        return db.query(Medico).filter(
            Medico.id_medico == id_medico
        ).first()

    def obtener_por_usuario(self, db: Session, id_usuario: int) -> Medico | None:
        """Verifica si un usuario ya está registrado como médico."""
        return db.query(Medico).filter(
            Medico.id_usuario == id_usuario
        ).first()

    def obtener_por_matricula(self, db: Session, matricula: str) -> Medico | None:
        """Verifica unicidad de matrícula a nivel global."""
        return db.query(Medico).filter(
            Medico.matricula == matricula
        ).first()

    def obtener_por_especialidad(
        self, db: Session, id_especialidad: int, id_hospital: int
    ) -> list[Medico]:
        """Filtra médicos por especialidad dentro de un hospital."""
        return db.query(Medico).filter(
            Medico.id_especialidad == id_especialidad,
            Medico.id_hospital == id_hospital,
            Medico.activo == True
        ).all()

    def crear(self, db: Session, medico: Medico) -> Medico:
        db.add(medico)
        db.commit()
        db.refresh(medico)
        return medico

    def actualizar(self, db: Session, medico: Medico) -> Medico:
        db.commit()
        db.refresh(medico)
        return medico

    def desactivar(self, db: Session, medico: Medico) -> Medico:
        """Baja lógica del médico."""
        medico.activo = False
        db.commit()
        db.refresh(medico)
        return medico