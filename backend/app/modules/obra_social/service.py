from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.obra_social.model import ObraSocial
from app.modules.obra_social.schema import ObraSocialCreate, ObraSocialUpdate
from app.modules.obra_social.repository import ObraSocialRepository

class ObraSocialService:

    def __init__(self):
        self.repository = ObraSocialRepository()

    def listar(self, db: Session) -> list[ObraSocial]:
        return self.repository.obtener_todas(db)

    def obtener_por_id(self, db: Session, id_obra_social: int) -> ObraSocial:
        os = self.repository.obtener_por_id(db, id_obra_social)
        if not os:
            raise HTTPException(status_code=404, detail=f"Obra social con id {id_obra_social} no encontrada.")
        return os

    def crear(self, db: Session, datos: ObraSocialCreate) -> ObraSocial:
        if self.repository.obtener_por_nombre(db, datos.nombre):
            raise HTTPException(status_code=400, detail=f"Ya existe una obra social con el nombre '{datos.nombre}'.")
        obra_social = ObraSocial(nombre=datos.nombre, activo=True)
        return self.repository.crear(db, obra_social)

    def actualizar(self, db: Session, id_obra_social: int, datos: ObraSocialUpdate) -> ObraSocial:
        obra_social = self.obtener_por_id(db, id_obra_social)
        if datos.nombre and datos.nombre != obra_social.nombre:
            if self.repository.obtener_por_nombre(db, datos.nombre):
                raise HTTPException(status_code=400, detail=f"Ya existe una obra social con el nombre '{datos.nombre}'.")
        campos = datos.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            setattr(obra_social, campo, valor)
        return self.repository.actualizar(db, obra_social)

    def desactivar(self, db: Session, id_obra_social: int) -> ObraSocial:
        obra_social = self.obtener_por_id(db, id_obra_social)
        return self.repository.desactivar(db, obra_social)

obra_social_service = ObraSocialService()