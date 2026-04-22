# =============================================================================
# modules/medico/service.py
# =============================================================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.medico.model import Medico
from app.modules.medico.schema import MedicoCreate, MedicoUpdate
from app.modules.medico.repository import MedicoRepository
from app.modules.usuario.repository import UsuarioRepository


class MedicoService:

    def __init__(self):
        self.repository = MedicoRepository()
        # Necesitamos el repository de Usuario para validar que el usuario exista
        self.usuario_repo = UsuarioRepository()

    def listar(self, db: Session, id_hospital: int) -> list[Medico]:
        return self.repository.obtener_todos(db, id_hospital)

    def listar_por_especialidad(
        self, db: Session, id_especialidad: int, id_hospital: int
    ) -> list[Medico]:
        return self.repository.obtener_por_especialidad(db, id_especialidad, id_hospital)

    def obtener_por_id(self, db: Session, id_medico: int) -> Medico:
        medico = self.repository.obtener_por_id(db, id_medico)
        if not medico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Médico con id {id_medico} no encontrado."
            )
        return medico

    def crear(self, db: Session, datos: MedicoCreate, id_hospital_admin: int) -> Medico:
        """
        Registra un médico asociándolo a un usuario existente.

        Reglas:
            - El usuario debe existir y pertenecer al mismo hospital
            - El usuario no puede estar ya registrado como médico
            - La matrícula debe ser única a nivel global
            - El hospital se fuerza desde el token del Admin (multi-tenant)
        """
        # Verificar que el usuario exista
        usuario = self.usuario_repo.obtener_por_id(db, datos.id_usuario)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id {datos.id_usuario} no encontrado."
            )

        # El usuario debe pertenecer al mismo hospital que el Admin
        if usuario.id_hospital != id_hospital_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario no pertenece a tu hospital."
            )

        # Verificar que el usuario no esté ya registrado como médico
        if self.repository.obtener_por_usuario(db, datos.id_usuario):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este usuario ya está registrado como médico."
            )

        # Verificar unicidad de matrícula
        if self.repository.obtener_por_matricula(db, datos.matricula):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un médico con la matrícula '{datos.matricula}'."
            )

        medico = Medico(
            id_usuario=datos.id_usuario,
            id_especialidad=datos.id_especialidad,
            id_hospital=id_hospital_admin,   # Siempre el hospital del Admin
            matricula=datos.matricula,
            activo=True
        )
        return self.repository.crear(db, medico)

    def actualizar(
        self, db: Session, id_medico: int, datos: MedicoUpdate, id_hospital_admin: int
    ) -> Medico:
        medico = self.obtener_por_id(db, id_medico)

        # El Admin solo puede modificar médicos de su hospital
        if medico.id_hospital != id_hospital_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No podés modificar médicos de otro hospital."
            )

        # Si se cambia la matrícula, verificar unicidad
        if datos.matricula and datos.matricula != medico.matricula:
            if self.repository.obtener_por_matricula(db, datos.matricula):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe un médico con la matrícula '{datos.matricula}'."
                )

        campos = datos.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            setattr(medico, campo, valor)

        return self.repository.actualizar(db, medico)

    def desactivar(self, db: Session, id_medico: int, id_hospital_admin: int) -> Medico:
        medico = self.obtener_por_id(db, id_medico)

        if medico.id_hospital != id_hospital_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No podés desactivar médicos de otro hospital."
            )

        return self.repository.desactivar(db, medico)


medico_service = MedicoService()