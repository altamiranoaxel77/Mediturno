# =============================================================================
# app/core/seed.py — Datos iniciales obligatorios del sistema
# =============================================================================

# IMPORTANTE: app.models debe ser el PRIMER import para que SQLAlchemy
# cargue todos los modelos en memoria antes de intentar usarlos.
import app.models  # noqa: F401

from app.database import SessionLocal
from app.modules.rol.model import Rol
from app.modules.dia_semana.model import DiaSemana


def seed_roles(db):
    """Inserta los 4 roles del sistema si no existen."""
    roles = [
        {"id_rol": 1, "nombre": "SuperAdmin"},
        {"id_rol": 2, "nombre": "Admin"},
        {"id_rol": 3, "nombre": "Secretario"},
        {"id_rol": 4, "nombre": "Doctor"},
    ]
    for datos in roles:
        existe = db.query(Rol).filter(Rol.id_rol == datos["id_rol"]).first()
        if not existe:
            db.add(Rol(**datos))
            print(f"  → Insertando rol: {datos['nombre']}")
        else:
            print(f"  → Ya existe rol: {datos['nombre']}")
    db.commit()
    print("✓ Roles OK")


def seed_dias_semana(db):
    """Inserta los 7 días de la semana si no existen."""
    dias = [
        {"id_dia": 1, "nombre": "Lunes"},
        {"id_dia": 2, "nombre": "Martes"},
        {"id_dia": 3, "nombre": "Miércoles"},
        {"id_dia": 4, "nombre": "Jueves"},
        {"id_dia": 5, "nombre": "Viernes"},
        {"id_dia": 6, "nombre": "Sábado"},
        {"id_dia": 7, "nombre": "Domingo"},
    ]
    for datos in dias:
        existe = db.query(DiaSemana).filter(DiaSemana.id_dia == datos["id_dia"]).first()
        if not existe:
            db.add(DiaSemana(**datos))
            print(f"  → Insertando día: {datos['nombre']}")
        else:
            print(f"  → Ya existe día: {datos['nombre']}")
    db.commit()
    print("✓ Días de la semana OK")


def run():
    print("Iniciando seed...")
    db = SessionLocal()
    try:
        seed_roles(db)
        seed_dias_semana(db)
        print("✓ Seed completado exitosamente")
    except Exception as e:
        print(f"✗ Error en seed: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    run()