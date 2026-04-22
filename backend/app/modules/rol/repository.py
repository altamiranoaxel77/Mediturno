from sqlalchemy.orm import Session
from app.modules.rol.model import Rol

class RolRepository:

    def obtener_todos(self, db: Session) -> list[Rol]:
        return db.query(Rol).filter(Rol.activo == True).all()

    def obtener_por_id(self, db: Session, id_rol: int) -> Rol | None:
        return db.query(Rol).filter(Rol.id_rol == id_rol, Rol.activo == True).first()