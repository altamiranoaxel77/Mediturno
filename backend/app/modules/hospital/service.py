# =============================================================================
# modules/hospital/service.py — Lógica de negocio para Hospital
# =============================================================================
# Responsabilidad: validaciones y reglas de negocio.
# El service no accede directamente a la BD — usa el repository.
# =============================================================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.hospital.model import Hospital
from app.modules.hospital.schema import HospitalCreate, HospitalUpdate
from app.modules.hospital.repository import HospitalRepository


class HospitalService:

    def __init__(self):
        self.repository = HospitalRepository()

    def listar(self, db: Session) -> list[Hospital]:
        """
        Retorna todos los hospitales activos del sistema.
        Solo accesible por SuperAdmin.
        """
        return self.repository.obtener_todos(db)

    def obtener_por_id(self, db: Session, id_hospital: int) -> Hospital:
        """
        Retorna un hospital por ID.
        Lanza 404 si no existe o está inactivo.
        """
        hospital = self.repository.obtener_por_id(db, id_hospital)
        if not hospital:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hospital con id {id_hospital} no encontrado."
            )
        return hospital

    def crear(self, db: Session, datos: HospitalCreate) -> Hospital:
        """
        Crea un nuevo hospital.

        Validaciones:
            - No puede existir otro hospital con el mismo nombre
        """
        # Verificar que no exista un hospital con el mismo nombre
        existe = self.repository.obtener_por_nombre(db, datos.nombre)
        if existe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un hospital con el nombre '{datos.nombre}'."
            )

        # Construir el objeto Hospital con los datos validados
        hospital = Hospital(
            nombre=datos.nombre,
            direccion=datos.direccion,
            telefono=datos.telefono,
            email=datos.email,
            activo=True
        )

        return self.repository.crear(db, hospital)

    def actualizar(
        self,
        db: Session,
        id_hospital: int,
        datos: HospitalUpdate
    ) -> Hospital:
        """
        Actualiza los datos de un hospital.
        Solo modifica los campos que vienen con valor (los None se ignoran).

        Validaciones:
            - El hospital debe existir
            - Si se cambia el nombre, no debe existir otro hospital con ese nombre
        """
        hospital = self.obtener_por_id(db, id_hospital)

        # Si se quiere cambiar el nombre, verificar que no esté en uso
        if datos.nombre and datos.nombre != hospital.nombre:
            existe = self.repository.obtener_por_nombre(db, datos.nombre)
            if existe:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe un hospital con el nombre '{datos.nombre}'."
                )

        # Actualizar solo los campos que vienen con valor
        # model_dump(exclude_unset=True) retorna solo los campos enviados en el request
        campos_a_actualizar = datos.model_dump(exclude_unset=True)
        for campo, valor in campos_a_actualizar.items():
            setattr(hospital, campo, valor)

        return self.repository.actualizar(db, hospital)

    def desactivar(self, db: Session, id_hospital: int) -> Hospital:
        """
        Baja lógica del hospital — cambia activo a False.

        Validaciones:
            - El hospital debe existir
        """
        hospital = self.obtener_por_id(db, id_hospital)
        return self.repository.desactivar(db, hospital)


# Instancia única del service
hospital_service = HospitalService()