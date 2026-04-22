# =============================================================================
# modules/turno/service.py
# =============================================================================

from datetime import date, time, datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.turno.model import Turno
from app.modules.turno.schema import TurnoCreate, TurnoUpdate, TurnoActualizarEstado, SlotDisponible
from app.modules.turno.repository import TurnoRepository
from app.modules.disponibilidad.repository import DisponibilidadRepository
from app.modules.paciente.repository import PacienteRepository
from app.modules.medico.repository import MedicoRepository


class TurnoService:

    def __init__(self):
        self.repository           = TurnoRepository()
        self.disponibilidad_repo  = DisponibilidadRepository()
        self.paciente_repo        = PacienteRepository()
        self.medico_repo          = MedicoRepository()

    # =========================================================================
    # Consultar slots disponibles
    # =========================================================================

    def obtener_slots_disponibles(
        self, db: Session, id_medico: int, fecha: date, id_hospital: int
    ) -> list[SlotDisponible]:
        """
        Calcula y retorna los horarios libres de un médico para una fecha dada.

        Proceso:
          1. Determinar el día de la semana de la fecha
          2. Obtener la disponibilidad del médico para ese día
          3. Generar todos los slots del rango horario
          4. Consultar los turnos ya ocupados
          5. Retornar solo los slots libres
        """
        # 1. Obtener el día de la semana (Python: 0=Lunes ... 6=Domingo)
        #    Nuestra BD usa: 1=Lunes ... 7=Domingo → sumamos 1
        dia_semana = fecha.weekday() + 1

        # 2. Obtener disponibilidad del médico para ese día
        disponibilidad = self.disponibilidad_repo.obtener_por_medico_y_dia(
            db, id_medico, dia_semana, id_hospital
        )

        if not disponibilidad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El médico no posee disponibilidad configurada para la fecha seleccionada."
            )

        # 3. Generar todos los slots posibles del día
        slots_totales = self._generar_slots(disponibilidad)

        if not slots_totales:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay horarios configurados para ese día."
            )

        # 4. Obtener turnos ya ocupados esa fecha
        turnos_ocupados = self.repository.obtener_por_medico_y_fecha(
            db, id_medico, fecha
        )

        # Construimos un set de horas ocupadas para búsqueda O(1)
        horas_ocupadas = {t.hora for t in turnos_ocupados}

        # 5. Filtrar y retornar solo los slots libres
        slots_libres = [
            slot for slot in slots_totales
            if slot.hora not in horas_ocupadas
        ]

        if not slots_libres:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay turnos disponibles para esta fecha."
            )

        return slots_libres

    # =========================================================================
    # Registrar turno
    # =========================================================================

    def crear(
        self, db: Session, datos: TurnoCreate, id_hospital: int
    ) -> Turno:
        """
        Registra un nuevo turno para un paciente.

        Validaciones:
          1. El médico existe y pertenece al hospital
          2. El paciente existe y pertenece al hospital
          3. El médico atiende ese día de la semana
          4. La hora está dentro del rango horario del médico
          5. No existe superposición con otro turno
        """
        # 1. Verificar médico
        medico = self.medico_repo.obtener_por_id(db, datos.id_medico)
        if not medico or medico.id_hospital != id_hospital:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Médico no encontrado en este hospital."
            )

        # 2. Verificar paciente
        paciente = self.paciente_repo.obtener_por_id(db, datos.id_paciente)
        if not paciente or paciente.id_hospital != id_hospital:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado en este hospital."
            )

        # 3. Verificar disponibilidad del médico ese día
        dia_semana = datos.fecha.weekday() + 1
        disponibilidad = self.disponibilidad_repo.obtener_por_medico_y_dia(
            db, datos.id_medico, dia_semana, id_hospital
        )

        if not disponibilidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El médico no atiende ese día de la semana."
            )

        # 4. Verificar que la hora esté dentro del rango horario
        if not self._hora_en_disponibilidad(datos.hora, disponibilidad):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "El horario seleccionado está fuera del rango de atención del médico. "
                    "Consultá los slots disponibles."
                )
            )

        # 5. Calcular hora_fin sumando la duración del turno
        hora_fin = self._calcular_hora_fin(
            datos.hora, disponibilidad.duracion_turno_minutos
        )

        # 6. Verificar que no haya superposición con otro turno
        if self.repository.verificar_superposicion(
            db, datos.id_medico, datos.fecha, datos.hora, hora_fin
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "El horario seleccionado ya no se encuentra disponible. "
                    "Por favor, elegí otro horario."
                )
            )

        # 7. Crear el turno
        turno = Turno(
            fecha=datos.fecha,
            hora=datos.hora,
            hora_fin=hora_fin,
            estado="pendiente",
            motivo_consulta=datos.motivo_consulta,
            id_paciente=datos.id_paciente,
            id_medico=datos.id_medico,
            id_hospital=id_hospital    # Siempre del usuario autenticado — multi-tenant
        )

        return self.repository.crear(db, turno)

    # =========================================================================
    # Consultar turnos
    # =========================================================================

    def obtener_por_id(self, db: Session, id_turno: int) -> Turno:
        turno = self.repository.obtener_por_id(db, id_turno)
        if not turno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Turno con id {id_turno} no encontrado."
            )
        return turno

    def obtener_agenda_medico(
        self, db: Session, id_medico: int, fecha: date, id_hospital: int
    ) -> list[Turno]:
        """
        Agenda del día de un médico.
        El Doctor solo puede ver su propia agenda — eso lo controla el router.
        """
        return self.repository.obtener_agenda_medico(db, id_medico, id_hospital, fecha)

    def obtener_por_paciente(
        self, db: Session, id_paciente: int, id_hospital: int
    ) -> list[Turno]:
        """Historial de turnos de un paciente."""
        paciente = self.paciente_repo.obtener_por_id(db, id_paciente)
        if not paciente or paciente.id_hospital != id_hospital:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado en este hospital."
            )
        return self.repository.obtener_por_paciente(db, id_paciente, id_hospital)

    # =========================================================================
    # Actualizar estado del turno
    # =========================================================================

    def actualizar_estado(
        self,
        db: Session,
        id_turno: int,
        datos: TurnoActualizarEstado,
        id_hospital: int
    ) -> Turno:
        """
        Cambia el estado de un turno.

        Transiciones válidas:
          pendiente → atendido   (el médico atendió al paciente)
          pendiente → cancelado  (el paciente o secretario cancela)
          pendiente → ausente    (el paciente no se presentó)

        No se puede modificar un turno ya atendido o cancelado.
        """
        turno = self.obtener_por_id(db, id_turno)

        # Verificar que el turno pertenece al hospital
        if turno.id_hospital != id_hospital:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No podés modificar turnos de otro hospital."
            )

        # No se puede modificar un turno ya cerrado
        if turno.estado in ["atendido", "cancelado"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede modificar un turno con estado '{turno.estado}'."
            )

        turno.estado = datos.estado
        if datos.observaciones:
            turno.observaciones = datos.observaciones

        return self.repository.actualizar(db, turno)

    def actualizar_datos(
        self, db: Session, id_turno: int, datos: TurnoUpdate, id_hospital: int
    ) -> Turno:
        """Actualiza el motivo de consulta u observaciones de un turno."""
        turno = self.obtener_por_id(db, id_turno)

        if turno.id_hospital != id_hospital:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No podés modificar turnos de otro hospital."
            )

        campos = datos.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            setattr(turno, campo, valor)

        return self.repository.actualizar(db, turno)

    # =========================================================================
    # Métodos privados
    # =========================================================================

    def _generar_slots(self, disponibilidad) -> list[SlotDisponible]:
        """
        Genera todos los slots horarios posibles a partir de la disponibilidad.

        Ejemplo: mañana 08:00-12:00 con duración 30 min
        → [08:00, 08:30, 09:00, 09:30, 10:00, 10:30, 11:00, 11:30]
        El slot de las 11:30 terminaría a las 12:00 — último válido.
        """
        slots = []
        duracion = disponibilidad.duracion_turno_minutos

        # Turno mañana
        if disponibilidad.turno_manana:
            slots += self._slots_en_rango(
                disponibilidad.hora_inicio_manana,
                disponibilidad.hora_fin_manana,
                duracion
            )

        # Turno tarde
        if disponibilidad.turno_tarde:
            slots += self._slots_en_rango(
                disponibilidad.hora_inicio_tarde,
                disponibilidad.hora_fin_tarde,
                duracion
            )

        return slots

    def _slots_en_rango(
        self, hora_inicio: time, hora_fin: time, duracion_minutos: int
    ) -> list[SlotDisponible]:
        """
        Genera slots de 'duracion_minutos' entre hora_inicio y hora_fin.
        Solo incluye slots que TERMINAN antes o exactamente en hora_fin.
        """
        slots = []

        # Convertir time a datetime para poder sumar timedelta
        base = datetime(2000, 1, 1)
        actual = datetime.combine(base, hora_inicio)
        fin    = datetime.combine(base, hora_fin)
        delta  = timedelta(minutes=duracion_minutos)

        while actual + delta <= fin:
            hora_slot     = actual.time()
            hora_fin_slot = (actual + delta).time()

            slots.append(SlotDisponible(hora=hora_slot, hora_fin=hora_fin_slot))
            actual += delta

        return slots

    def _hora_en_disponibilidad(self, hora: time, disponibilidad) -> bool:
        """
        Verifica que la hora solicitada esté dentro del rango de atención.
        Chequea tanto el turno mañana como el turno tarde.
        """
        if disponibilidad.turno_manana:
            if disponibilidad.hora_inicio_manana <= hora < disponibilidad.hora_fin_manana:
                return True

        if disponibilidad.turno_tarde:
            if disponibilidad.hora_inicio_tarde <= hora < disponibilidad.hora_fin_tarde:
                return True

        return False

    def _calcular_hora_fin(self, hora: time, duracion_minutos: int) -> time:
        """
        Suma la duración al horario de inicio para obtener la hora de fin del turno.
        Ejemplo: 09:00 + 30 min → 09:30
        """
        base = datetime(2000, 1, 1)
        dt_inicio = datetime.combine(base, hora)
        dt_fin    = dt_inicio + timedelta(minutes=duracion_minutos)
        return dt_fin.time()


turno_service = TurnoService()