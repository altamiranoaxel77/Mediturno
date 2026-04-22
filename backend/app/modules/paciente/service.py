# =============================================================================
# modules/paciente/service.py
# =============================================================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.paciente.model import Paciente
from app.modules.paciente.schema import PacienteCreate, PacienteUpdate
from app.modules.paciente.repository import PacienteRepository


class PacienteService:

    def __init__(self):
        self.repository = PacienteRepository()

    def listar(self, db: Session, id_hospital: int) -> list[Paciente]:
        return self.repository.obtener_todos(db, id_hospital)

    def obtener_por_id(self, db: Session, id_paciente: int) -> Paciente:
        paciente = self.repository.obtener_por_id(db, id_paciente)
        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Paciente con id {id_paciente} no encontrado."
            )
        return paciente

    def obtener_por_dni(self, db: Session, dni: str, id_hospital: int) -> Paciente:
        """
        Busca un paciente por DNI. Usado al registrar un turno para
        verificar que el paciente existe en el hospital.
        """
        paciente = self.repository.obtener_por_dni(db, dni, id_hospital)
        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe un paciente con DNI '{dni}' en este hospital."
            )
        return paciente

    def crear(self, db: Session, datos: PacienteCreate, id_hospital: int) -> Paciente:
        """
        Registra un paciente en el hospital.

        Reglas:
            - El DNI debe ser único dentro del hospital
            - El hospital se fuerza desde el token JWT (multi-tenant)
        """
        # DNI único por hospital (un mismo paciente puede estar en dos hospitales)
        if self.repository.obtener_por_dni(db, datos.dni, id_hospital):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un paciente con DNI '{datos.dni}' en este hospital."
            )

        paciente = Paciente(
            nombre=datos.nombre,
            apellido=datos.apellido,
            dni=datos.dni,
            telefono=datos.telefono,
            email=datos.email,
            fecha_nacimiento=datos.fecha_nacimiento,
            id_obra_social=datos.id_obra_social,
            id_hospital=id_hospital,   # Siempre el hospital del usuario autenticado
            activo=True
        )
        return self.repository.crear(db, paciente)

    def actualizar(
        self, db: Session, id_paciente: int, datos: PacienteUpdate, id_hospital: int
    ) -> Paciente:
        paciente = self.obtener_por_id(db, id_paciente)

        # Solo se pueden modificar pacientes del mismo hospital
        if paciente.id_hospital != id_hospital:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No podés modificar pacientes de otro hospital."
            )

        campos = datos.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            setattr(paciente, campo, valor)

        return self.repository.actualizar(db, paciente)

    def desactivar(self, db: Session, id_paciente: int, id_hospital: int) -> Paciente:
        paciente = self.obtener_por_id(db, id_paciente)

        if paciente.id_hospital != id_hospital:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No podés desactivar pacientes de otro hospital."
            )

        return self.repository.desactivar(db, paciente)


paciente_service = PacienteService()