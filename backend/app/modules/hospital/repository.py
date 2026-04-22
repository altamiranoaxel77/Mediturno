# =============================================================================
# modules/hospital/repository.py — Acceso a datos para Hospital
# =============================================================================
# Responsabilidad: SOLO consultas a la base de datos.
# Sin lógica de negocio — eso va en el service.
# =============================================================================

from sqlalchemy.orm import Session
from app.modules.hospital.model import Hospital


class HospitalRepository:

    def obtener_todos(self, db: Session) -> list[Hospital]:
        """
        Retorna todos los hospitales activos del sistema.
        Solo el SuperAdmin llama a este método — ve TODOS los hospitales.
        """
        return db.query(Hospital).filter(
            Hospital.activo == True
        ).all()

    def obtener_por_id(self, db: Session, id_hospital: int) -> Hospital | None:
        """
        Busca un hospital por su ID.
        Retorna None si no existe o está inactivo.
        """
        return db.query(Hospital).filter(
            Hospital.id_hospital == id_hospital,
            Hospital.activo == True
        ).first()

    def obtener_por_nombre(self, db: Session, nombre: str) -> Hospital | None:
        """
        Busca un hospital por nombre exacto (case-insensitive).
        Se usa para validar que no existan hospitales duplicados.
        """
        return db.query(Hospital).filter(
            Hospital.nombre.ilike(nombre),  # ilike = case-insensitive LIKE
            Hospital.activo == True
        ).first()

    def crear(self, db: Session, hospital: Hospital) -> Hospital:
        """
        Persiste un nuevo hospital en la base de datos.
        Recibe el objeto ya construido desde el service.
        """
        db.add(hospital)
        db.commit()
        # refresh actualiza el objeto con los datos generados por la BD
        # (como el id_hospital autoincremental)
        db.refresh(hospital)
        return hospital

    def actualizar(self, db: Session, hospital: Hospital) -> Hospital:
        """
        Guarda los cambios de un hospital ya modificado.
        El service modifica los atributos del objeto y llama a este método.
        """
        db.commit()
        db.refresh(hospital)
        return hospital

    def desactivar(self, db: Session, hospital: Hospital) -> Hospital:
        """
        Baja lógica — marca el hospital como inactivo.
        No elimina el registro de la base de datos.
        """
        hospital.activo = False
        db.commit()
        db.refresh(hospital)
        return hospital