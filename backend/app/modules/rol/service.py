from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modules.rol.model import Rol
from app.modules.rol.repository import RolRepository

class RolService:

    def __init__(self):
        self.repository = RolRepository()

    def listar(self, db: Session) -> list[Rol]:
        return self.repository.obtener_todos(db)

    def obtener_por_id(self, db: Session, id_rol: int) -> Rol:
        rol = self.repository.obtener_por_id(db, id_rol)
        if not rol:
            raise HTTPException(status_code=404, detail=f"Rol con id {id_rol} no encontrado.")
        return rol

rol_service = RolService()