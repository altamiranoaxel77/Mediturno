# =============================================================================
# modules/disponibilidad/service.py
# =============================================================================

from datetime import time
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.disponibilidad.model import DisponibilidadMedico
from app.modules.disponibilidad.schema import DisponibilidadCreate, DisponibilidadUpdate
from app.modules.disponibilidad.repository import DisponibilidadRepository
from app.modules.medico.repository import MedicoRepository


class DisponibilidadService:

    def __init__(self):
        self.repository = DisponibilidadRepository()
        self.medico_repo = MedicoRepository()

    def listar_por_medico(
        self, db: Session, id_medico: int, id_hospital: int
    ) -> list[DisponibilidadMedico]:
        """Retorna la agenda semanal completa de un médico."""
        return self.repository.obtener_por_medico(db, id_medico, id_hospital)

    def obtener_por_id(
        self, db: Session, id_disponibilidad: int
    ) -> DisponibilidadMedico:
        disp = self.repository.obtener_por_id(db, id_disponibilidad)
        if not disp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Disponibilidad con id {id_disponibilidad} no encontrada."
            )
        return disp

    def crear(
        self,
        db: Session,
        datos: DisponibilidadCreate,
        id_hospital: int
    ) -> DisponibilidadMedico:
        """
        Configura la disponibilidad de un médico para un día de la semana.

        Validaciones:
            1. El médico debe existir y pertenecer al hospital
            2. No puede existir otra disponibilidad activa para ese médico+día+hospital
            3. Si turno_manana=True → hora_inicio_manana < hora_fin_manana
            4. Si turno_tarde=True  → hora_inicio_tarde  < hora_fin_tarde
            5. Si ambos turnos activos → turno mañana debe terminar antes que empiece el tarde
        """
        # 1. Verificar que el médico existe y pertenece al hospital
        medico = self.medico_repo.obtener_por_id(db, datos.id_medico)
        if not medico or medico.id_hospital != id_hospital:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Médico no encontrado en este hospital."
            )

        # 2. Verificar que no exista disponibilidad para ese día
        existe = self.repository.obtener_por_medico_y_dia(
            db, datos.id_medico, datos.id_dia, id_hospital
        )
        if existe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Ya existe una disponibilidad configurada para este médico "
                    "en ese día. Modificá la existente o desactivala primero."
                )
            )

        # 3 y 4. Validar coherencia de horarios (el schema ya valida básico,
        # aquí validamos la lógica de superposición entre turnos)
        self._validar_horarios(datos)

        disponibilidad = DisponibilidadMedico(
            id_medico=datos.id_medico,
            id_dia=datos.id_dia,
            id_hospital=id_hospital,
            turno_manana=datos.turno_manana,
            hora_inicio_manana=datos.hora_inicio_manana,
            hora_fin_manana=datos.hora_fin_manana,
            turno_tarde=datos.turno_tarde,
            hora_inicio_tarde=datos.hora_inicio_tarde,
            hora_fin_tarde=datos.hora_fin_tarde,
            duracion_turno_minutos=datos.duracion_turno_minutos,
            activo=True
        )
        return self.repository.crear(db, disponibilidad)

    def actualizar(
        self,
        db: Session,
        id_disponibilidad: int,
        datos: DisponibilidadUpdate,
        id_hospital: int
    ) -> DisponibilidadMedico:
        """
        Modifica la disponibilidad existente de un médico para un día.
        Solo se actualizan los campos enviados.
        """
        disponibilidad = self.obtener_por_id(db, id_disponibilidad)

        # Solo se puede modificar disponibilidad del mismo hospital
        if disponibilidad.id_hospital != id_hospital:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No podés modificar disponibilidades de otro hospital."
            )

        # Aplicar los cambios
        campos = datos.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            setattr(disponibilidad, campo, valor)

        # Revalidar horarios con los datos actualizados
        self._validar_horarios_objeto(disponibilidad)

        return self.repository.actualizar(db, disponibilidad)

    def desactivar(
        self, db: Session, id_disponibilidad: int, id_hospital: int
    ) -> DisponibilidadMedico:
        """
        Baja lógica de la disponibilidad.
        El médico deja de atender ese día — sus turnos futuros no se cancelan
        automáticamente (eso lo gestiona el secretario manualmente).
        """
        disponibilidad = self.obtener_por_id(db, id_disponibilidad)

        if disponibilidad.id_hospital != id_hospital:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No podés desactivar disponibilidades de otro hospital."
            )

        return self.repository.desactivar(db, disponibilidad)

    # ── Métodos privados de validación ────────────────────────────────────────

    def _validar_horarios(self, datos: DisponibilidadCreate) -> None:
        """
        Valida la coherencia de los horarios de un turno.
        El @model_validator del schema ya verifica que los campos obligatorios
        estén presentes. Aquí validamos la superposición entre turnos.
        """
        if datos.turno_manana and datos.turno_tarde:
            # El turno mañana debe terminar antes de que empiece el turno tarde
            if datos.hora_fin_manana >= datos.hora_inicio_tarde:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "El turno mañana se superpone con el turno tarde. "
                        "La hora de fin de mañana debe ser anterior a la hora "
                        "de inicio de tarde."
                    )
                )

    def _validar_horarios_objeto(self, disp: DisponibilidadMedico) -> None:
        """
        Misma validación pero sobre el objeto SQLAlchemy después de aplicar updates.
        """
        if disp.turno_manana and disp.turno_tarde:
            if disp.hora_fin_manana and disp.hora_inicio_tarde:
                if disp.hora_fin_manana >= disp.hora_inicio_tarde:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=(
                            "El turno mañana se superpone con el turno tarde."
                        )
                    )


disponibilidad_service = DisponibilidadService()