# =============================================================================
# modules/especialidad/service.py
# =============================================================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.especialidad.model import Especialidad
from app.modules.especialidad.schema import EspecialidadCreate, EspecialidadUpdate
from app.modules.especialidad.repository import EspecialidadRepository


class EspecialidadService:

    def __init__(self):
        self.repository = EspecialidadRepository()

    def listar(self, db: Session) -> list[Especialidad]:
        return self.repository.obtener_todas(db)

    def obtener_por_id(self, db: Session, id_especialidad: int) -> Especialidad:
        esp = self.repository.obtener_por_id(db, id_especialidad)
        if not esp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Especialidad con id {id_especialidad} no encontrada."
            )
        return esp

    def crear(self, db: Session, datos: EspecialidadCreate) -> Especialidad:
        if self.repository.obtener_por_nombre(db, datos.nombre):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una especialidad con el nombre '{datos.nombre}'."
            )
        especialidad = Especialidad(nombre=datos.nombre, activo=True)
        return self.repository.crear(db, especialidad)

    def actualizar(self, db: Session, id_especialidad: int, datos: EspecialidadUpdate) -> Especialidad:
        especialidad = self.obtener_por_id(db, id_especialidad)
        if datos.nombre and datos.nombre != especialidad.nombre:
            if self.repository.obtener_por_nombre(db, datos.nombre):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe una especialidad con el nombre '{datos.nombre}'."
                )
        campos = datos.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            setattr(especialidad, campo, valor)
        return self.repository.actualizar(db, especialidad)

    def desactivar(self, db: Session, id_especialidad: int) -> Especialidad:
        especialidad = self.obtener_por_id(db, id_especialidad)
        return self.repository.desactivar(db, especialidad)


especialidad_service = EspecialidadService()