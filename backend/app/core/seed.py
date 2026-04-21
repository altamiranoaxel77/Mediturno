# =============================================================================
# app/core/seed.py — Datos iniciales obligatorios del sistema
# =============================================================================
# Este script inserta los registros base que el sistema necesita para funcionar.
# Se ejecuta UNA SOLA VEZ después de aplicar las migraciones:
#
#   python -m app.core.seed
#
# Qué hace:
#   1. Inserta los 4 roles del sistema
#   2. Inserta los 7 días de la semana
#   3. Crea el usuario SuperAdmin (sin hospital — es el dueño de la plataforma)
# =============================================================================

# IMPORTANTE: app.models debe ser el PRIMER import para que SQLAlchemy
# cargue todos los modelos en memoria antes de intentar usarlos.
import app.models  # noqa: F401

from app.database import SessionLocal
from app.modules.rol.model import Rol
from app.modules.dia_semana.model import DiaSemana
from app.modules.usuario.model import Usuario
from app.core.security import hashear_password


def seed_roles(db) -> None:
    """
    Inserta los 4 roles del sistema si no existen.
    Los roles son fijos y no deben modificarse.
    """
    roles = [
        {"id_rol": 1, "nombre": "SuperAdmin"},  # Dueño de la plataforma — sin hospital
        {"id_rol": 2, "nombre": "Admin"},        # Administrador de un hospital
        {"id_rol": 3, "nombre": "Secretario"},   # Gestiona turnos y disponibilidades
        {"id_rol": 4, "nombre": "Doctor"},       # Ve su propia agenda de turnos
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


def seed_dias_semana(db) -> None:
    """
    Inserta los 7 días de la semana si no existen.
    Se usan en la tabla disponibilidad_medico.
    Convenio: 1=Lunes ... 7=Domingo
    """
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


def seed_superadmin(db) -> None:
    """
    Crea el usuario SuperAdmin si no existe.

    El SuperAdmin:
    - Tiene id_rol=1 (SuperAdmin)
    - NO tiene hospital (id_hospital=None) — es el dueño de la plataforma
    - Es el único usuario que puede tener id_hospital=None (CHECK CONSTRAINT en BD)
    - Crea hospitales y sus administradores
    """
    existe = db.query(Usuario).filter(
        Usuario.email == "superadmin@mediturno.com"
    ).first()

    if existe:
        print("  → Ya existe el usuario SuperAdmin")
        return

    superadmin = Usuario(
        nombre="Super",
        apellido="Admin",
        dni="00000001",
        email="superadmin@mediturno.com",
        password=hashear_password("Admin1234"),
        id_rol=1,
        id_hospital=None,  # El SuperAdmin no pertenece a ningún hospital
        activo=True
    )
    db.add(superadmin)
    db.commit()
    print("  → SuperAdmin creado")
    print("     Email:    superadmin@mediturno.com")
    print("     Password: Admin1234")
    print("     IMPORTANTE: cambiá la contraseña después del primer login")
    print("✓ SuperAdmin OK")


def run() -> None:
    """Ejecuta todas las funciones de seed en orden."""
    print("\nIniciando seed del sistema Mediturno...")
    print("=" * 50)

    db = SessionLocal()
    try:
        print("\n[1/3] Roles:")
        seed_roles(db)

        print("\n[2/3] Días de la semana:")
        seed_dias_semana(db)

        print("\n[3/3] Usuario SuperAdmin:")
        seed_superadmin(db)

        print("\n" + "=" * 50)
        print("✓ Seed completado exitosamente")
        print("  El sistema está listo para usar.\n")

    except Exception as e:
        print(f"\n✗ Error en seed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run()