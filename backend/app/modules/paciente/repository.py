# =============================================================================
# modules/paciente/repository.py
# =============================================================================

from sqlalchemy.orm import Session
from app.modules.paciente.model import Paciente


class PacienteRepository:

    def obtener_todos(self, db: Session, id_hospital: int) -> list[Paciente]:
        """Retorna todos los pacientes activos de un hospital — multi-tenant."""
        return db.query(Paciente).filter(
            Paciente.id_hospital == id_hospital,
            Paciente.activo == True
        ).all()

    def obtener_por_id(self, db: Session, id_paciente: int) -> Paciente | None:
        return db.query(Paciente).filter(
            Paciente.id_paciente == id_paciente
        ).first()

    def obtener_por_dni(
        self, db: Session, dni: str, id_hospital: int
    ) -> Paciente | None:
        """Busca un paciente por DNI dentro de un hospital."""
        return db.query(Paciente).filter(
            Paciente.dni == dni,
            Paciente.id_hospital == id_hospital
        ).first()

    def crear(self, db: Session, paciente: Paciente) -> Paciente:
        db.add(paciente)
        db.commit()
        db.refresh(paciente)
        return paciente

    def actualizar(self, db: Session, paciente: Paciente) -> Paciente:
        db.commit()
        db.refresh(paciente)
        return paciente

    def desactivar(self, db: Session, paciente: Paciente) -> Paciente:
        paciente.activo = False
        db.commit()
        db.refresh(paciente)
        return paciente