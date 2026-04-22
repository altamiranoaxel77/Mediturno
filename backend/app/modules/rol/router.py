from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user
from app.modules.rol.schema import RolResponse
from app.modules.rol.service import rol_service

router = APIRouter()

@router.get("/", response_model=list[RolResponse], summary="Listar roles")
def listar_roles(db: Session = Depends(get_db), _=Depends(get_current_user)):
    # Cualquier usuario autenticado puede ver los roles (para asignar al crear usuarios)
    return rol_service.listar(db)

@router.get("/{id_rol}", response_model=RolResponse)
def obtener_rol(id_rol: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return rol_service.obtener_por_id(db, id_rol)