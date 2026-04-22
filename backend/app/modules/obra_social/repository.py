from sqlalchemy.orm import Session
from app.modules.obra_social.model import ObraSocial

class ObraSocialRepository:

    def obtener_todas(self, db: Session) -> list[ObraSocial]:
        return db.query(ObraSocial).filter(ObraSocial.activo == True).all()

    def obtener_por_id(self, db: Session, id_obra_social: int) -> ObraSocial | None:
        return db.query(ObraSocial).filter(
            ObraSocial.id_obra_social == id_obra_social,
            ObraSocial.activo == True
        ).first()

    def obtener_por_nombre(self, db: Session, nombre: str) -> ObraSocial | None:
        return db.query(ObraSocial).filter(ObraSocial.nombre.ilike(nombre)).first()

    def crear(self, db: Session, obra_social: ObraSocial) -> ObraSocial:
        db.add(obra_social)
        db.commit()
        db.refresh(obra_social)
        return obra_social

    def actualizar(self, db: Session, obra_social: ObraSocial) -> ObraSocial:
        db.commit()
        db.refresh(obra_social)
        return obra_social

    def desactivar(self, db: Session, obra_social: ObraSocial) -> ObraSocial:
        obra_social.activo = False
        db.commit()
        db.refresh(obra_social)
        return obra_social