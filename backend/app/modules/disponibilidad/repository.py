# =============================================================================
# modules/disponibilidad/repository.py
# =============================================================================

from sqlalchemy.orm import Session
from app.modules.disponibilidad.model import DisponibilidadMedico


class DisponibilidadRepository:

    def obtener_por_medico(
        self, db: Session, id_medico: int, id_hospital: int
    ) -> list[DisponibilidadMedico]:
        """
        Retorna toda la agenda semanal de un médico.
        Se usa para mostrar qué días y horarios atiende.
        """
        return db.query(DisponibilidadMedico).filter(
            DisponibilidadMedico.id_medico == id_medico,
            DisponibilidadMedico.id_hospital == id_hospital,
            DisponibilidadMedico.activo == True
        ).all()

    def obtener_por_medico_y_dia(
        self, db: Session, id_medico: int, id_dia: int, id_hospital: int
    ) -> DisponibilidadMedico | None:
        """
        Retorna la disponibilidad de un médico para un día específico.
        Se usa al calcular los slots disponibles para una fecha dada.
        """
        return db.query(DisponibilidadMedico).filter(
            DisponibilidadMedico.id_medico == id_medico,
            DisponibilidadMedico.id_dia == id_dia,
            DisponibilidadMedico.id_hospital == id_hospital,
            DisponibilidadMedico.activo == True
        ).first()

    def obtener_por_id(
        self, db: Session, id_disponibilidad: int
    ) -> DisponibilidadMedico | None:
        return db.query(DisponibilidadMedico).filter(
            DisponibilidadMedico.id_disponibilidad == id_disponibilidad
        ).first()

    def crear(
        self, db: Session, disponibilidad: DisponibilidadMedico
    ) -> DisponibilidadMedico:
        db.add(disponibilidad)
        db.commit()
        db.refresh(disponibilidad)
        return disponibilidad

    def actualizar(
        self, db: Session, disponibilidad: DisponibilidadMedico
    ) -> DisponibilidadMedico:
        db.commit()
        db.refresh(disponibilidad)
        return disponibilidad

    def desactivar(
        self, db: Session, disponibilidad: DisponibilidadMedico
    ) -> DisponibilidadMedico:
        """Baja lógica — el médico deja de atender ese día."""
        disponibilidad.activo = False
        db.commit()
        db.refresh(disponibilidad)
        return disponibilidad