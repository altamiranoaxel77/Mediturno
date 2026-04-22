from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import require_roles
from app.core.roles import Roles
from app.modules.obra_social.schema import ObraSocialCreate, ObraSocialUpdate, ObraSocialResponse
from app.modules.obra_social.service import obra_social_service

router = APIRouter()
solo_superadmin = Depends(require_roles(Roles.SUPERADMIN))

@router.get("/", response_model=list[ObraSocialResponse], summary="Listar obras sociales")
def listar_obras_sociales(db: Session = Depends(get_db)):
    return obra_social_service.listar(db)

@router.get("/{id_obra_social}", response_model=ObraSocialResponse)
def obtener_obra_social(id_obra_social: int, db: Session = Depends(get_db)):
    return obra_social_service.obtener_por_id(db, id_obra_social)

@router.post("/", response_model=ObraSocialResponse, status_code=status.HTTP_201_CREATED)
def crear_obra_social(datos: ObraSocialCreate, db: Session = Depends(get_db), _: None = solo_superadmin):
    return obra_social_service.crear(db, datos)

@router.put("/{id_obra_social}", response_model=ObraSocialResponse)
def actualizar_obra_social(id_obra_social: int, datos: ObraSocialUpdate, db: Session = Depends(get_db), _: None = solo_superadmin):
    return obra_social_service.actualizar(db, id_obra_social, datos)

@router.put("/{id_obra_social}/desactivar", response_model=ObraSocialResponse)
def desactivar_obra_social(id_obra_social: int, db: Session = Depends(get_db), _: None = solo_superadmin):
    return obra_social_service.desactivar(db, id_obra_social)