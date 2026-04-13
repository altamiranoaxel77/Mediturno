import app.models
from app.database import SessionLocal
from app.modules.usuario.model import Usuario
from app.core.security import hashear_password

def run():
    db = SessionLocal()
    try:
        existe = db.query(Usuario).filter(
            Usuario.email == "superadmin@mediturno.com"
        ).first()

        if existe:
            print("El usuario SuperAdmin ya existe")
            return

        usuario = Usuario(
            nombre="Super",
            apellido="Admin",
            dni="00000001",
            email="superadmin@mediturno.com",
            password=hashear_password("Admin1234"),
            id_rol=1,
            id_hospital=1,
            activo=True
        )
        db.add(usuario)
        db.commit()
        print("Usuario SuperAdmin creado correctamente")
        print("Email:    superadmin@mediturno.com")
        print("Password: Admin1234")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run()