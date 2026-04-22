# =============================================================================
# modules/turno/repository.py
# =============================================================================

from datetime import date, time
from sqlalchemy.orm import Session
from app.modules.turno.model import Turno


class TurnoRepository:

    def obtener_por_medico_y_fecha(
        self, db: Session, id_medico: int, fecha: date
    ) -> list[Turno]:
        """
        Retorna todos los turnos de un médico en una fecha específica.
        Se usa para calcular qué horarios ya están ocupados y excluirlos
        de los slots disponibles.
        Incluye turnos pendientes y atendidos — NO los cancelados ni ausentes.
        """
        return db.query(Turno).filter(
            Turno.id_medico == id_medico,
            Turno.fecha == fecha,
            Turno.estado.in_(["pendiente", "atendido"])
        ).all()

    def verificar_superposicion(
        self,
        db: Session,
        id_medico: int,
        fecha: date,
        hora: time,
        hora_fin: time,
        id_turno_excluir: int | None = None
    ) -> bool:
        """
        Verifica si existe algún turno que se superponga con el horario dado.

        Un turno se superpone si:
            - El nuevo turno empieza DENTRO de un turno existente, O
            - El nuevo turno termina DENTRO de un turno existente, O
            - El nuevo turno contiene completamente a un turno existente

        id_turno_excluir: se usa al actualizar un turno para no compararlo consigo mismo.
        """
        query = db.query(Turno).filter(
            Turno.id_medico == id_medico,
            Turno.fecha == fecha,
            Turno.estado.in_(["pendiente", "atendido"]),
            # Condición de superposición: los rangos se pisan si
            # el inicio del nuevo es menor al fin del existente
            # Y el fin del nuevo es mayor al inicio del existente
            Turno.hora < hora_fin,
            Turno.hora_fin > hora
        )
        if id_turno_excluir:
            query = query.filter(Turno.id_turno != id_turno_excluir)

        return query.first() is not None

    def obtener_por_id(self, db: Session, id_turno: int) -> Turno | None:
        return db.query(Turno).filter(
            Turno.id_turno == id_turno
        ).first()

    def obtener_por_paciente(
        self, db: Session, id_paciente: int, id_hospital: int
    ) -> list[Turno]:
        """Historial de turnos de un paciente en un hospital."""
        return db.query(Turno).filter(
            Turno.id_paciente == id_paciente,
            Turno.id_hospital == id_hospital
        ).order_by(Turno.fecha.desc(), Turno.hora.desc()).all()

    def obtener_por_medico_rango(
        self,
        db: Session,
        id_medico: int,
        id_hospital: int,
        fecha_desde: date,
        fecha_hasta: date
    ) -> list[Turno]:
        """
        Retorna los turnos de un médico en un rango de fechas.
        Se usa para la agenda del doctor y para el listado del secretario.
        """
        return db.query(Turno).filter(
            Turno.id_medico == id_medico,
            Turno.id_hospital == id_hospital,
            Turno.fecha >= fecha_desde,
            Turno.fecha <= fecha_hasta
        ).order_by(Turno.fecha, Turno.hora).all()

    def obtener_agenda_medico(
        self, db: Session, id_medico: int, id_hospital: int, fecha: date
    ) -> list[Turno]:
        """
        Retorna los turnos de un médico para una fecha específica.
        Se usa en la vista de agenda del Doctor.
        """
        return db.query(Turno).filter(
            Turno.id_medico == id_medico,
            Turno.id_hospital == id_hospital,
            Turno.fecha == fecha
        ).order_by(Turno.hora).all()

    def crear(self, db: Session, turno: Turno) -> Turno:
        db.add(turno)
        db.commit()
        db.refresh(turno)
        return turno

    def actualizar(self, db: Session, turno: Turno) -> Turno:
        db.commit()
        db.refresh(turno)
        return turno