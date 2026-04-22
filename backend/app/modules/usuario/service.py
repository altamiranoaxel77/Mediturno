# =============================================================================
# modules/usuario/service.py — Lógica de negocio para Usuario
# =============================================================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.usuario.model import Usuario
from app.modules.usuario.schema import UsuarioCreate, UsuarioUpdate
from app.modules.usuario.repository import UsuarioRepository
from app.core.security import hashear_password
from app.core.roles import Roles


class UsuarioService:

    def __init__(self):
        self.repository = UsuarioRepository()

    def listar(self, db: Session, id_hospital: int) -> list[Usuario]:
        """
        Retorna todos los usuarios activos de un hospital.
        Solo Admin y SuperAdmin pueden listar usuarios.
        """
        return self.repository.obtener_todos(db, id_hospital)

    def obtener_por_id(self, db: Session, id_usuario: int) -> Usuario:
        """
        Retorna un usuario por ID.
        Lanza 404 si no existe.
        """
        usuario = self.repository.obtener_por_id(db, id_usuario)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id {id_usuario} no encontrado."
            )
        return usuario

    def crear(
        self,
        db: Session,
        datos: UsuarioCreate,
        rol_creador: str,
        id_hospital_creador: int | None
    ) -> Usuario:
        """
        Crea un nuevo usuario aplicando las reglas de negocio según el rol del creador.

        Reglas:
            - Admin solo puede crear Secretario y Doctor en su propio hospital
            - SuperAdmin puede crear Admin (con hospital obligatorio)
            - Nadie puede crear otro SuperAdmin desde la API
            - DNI y email deben ser únicos a nivel global
        """
        # ── Validar qué roles puede crear el usuario actual ───────────────────

        if rol_creador == Roles.ADMIN:
            # El Admin solo puede crear Secretario (3) o Doctor (4)
            if datos.id_rol not in [3, 4]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Un Admin solo puede crear usuarios con rol Secretario o Doctor."
                )
            # El Admin no puede asignar otro hospital — se fuerza el suyo
            id_hospital_final = id_hospital_creador

        elif rol_creador == Roles.SUPERADMIN:
            # El SuperAdmin no puede crear otro SuperAdmin desde la API
            if datos.id_rol == 1:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No se puede crear otro SuperAdmin desde la API."
                )
            # El SuperAdmin crea Admins — el hospital es obligatorio para ellos
            if datos.id_rol == 2 and not datos.id_hospital:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Para crear un Admin debe especificarse el id_hospital."
                )
            id_hospital_final = datos.id_hospital

        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tenés permisos para crear usuarios."
            )

        # ── Validar unicidad de email ─────────────────────────────────────────
        if self.repository.obtener_por_email(db, datos.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un usuario con el email '{datos.email}'."
            )

        # ── Validar unicidad de DNI ───────────────────────────────────────────
        if self.repository.obtener_por_dni(db, datos.dni):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un usuario con el DNI '{datos.dni}'."
            )

        # ── Construir el objeto Usuario ───────────────────────────────────────
        usuario = Usuario(
            nombre=datos.nombre,
            apellido=datos.apellido,
            dni=datos.dni,
            email=datos.email,
            # Hasheamos la contraseña — NUNCA se guarda en texto plano
            password=hashear_password(datos.password),
            id_rol=datos.id_rol,
            id_hospital=id_hospital_final,
            activo=True
        )

        return self.repository.crear(db, usuario)

    def actualizar(
        self,
        db: Session,
        id_usuario: int,
        datos: UsuarioUpdate,
        rol_creador: str,
        id_hospital_creador: int | None
    ) -> Usuario:
        """
        Actualiza los datos de un usuario.

        Reglas:
            - Admin solo puede modificar usuarios de su hospital
            - Si se cambia el email, no debe existir otro usuario con ese email
            - Si se cambia la contraseña, se vuelve a hashear
        """
        usuario = self.obtener_por_id(db, id_usuario)

        # El Admin no puede modificar usuarios de otro hospital
        if rol_creador == Roles.ADMIN:
            if usuario.id_hospital != id_hospital_creador:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No podés modificar usuarios de otro hospital."
                )

        # Validar unicidad de email si se quiere cambiar
        if datos.email and datos.email != usuario.email:
            if self.repository.obtener_por_email(db, datos.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe un usuario con el email '{datos.email}'."
                )

        # Actualizar solo los campos enviados
        campos = datos.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            # Si se actualiza la contraseña, hashearla antes de guardar
            if campo == "password":
                setattr(usuario, campo, hashear_password(valor))
            else:
                setattr(usuario, campo, valor)

        return self.repository.actualizar(db, usuario)

    def desactivar(
        self,
        db: Session,
        id_usuario: int,
        rol_creador: str,
        id_hospital_creador: int | None
    ) -> Usuario:
        """
        Baja lógica del usuario — cambia activo a False.

        Reglas:
            - Admin solo puede desactivar usuarios de su hospital
            - No se puede desactivar al SuperAdmin
        """
        usuario = self.obtener_por_id(db, id_usuario)

        # No se puede desactivar al SuperAdmin
        if usuario.id_rol == 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No se puede desactivar al SuperAdmin."
            )

        # El Admin solo puede desactivar usuarios de su hospital
        if rol_creador == Roles.ADMIN:
            if usuario.id_hospital != id_hospital_creador:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No podés desactivar usuarios de otro hospital."
                )

        return self.repository.desactivar(db, usuario)


# Instancia única del service
usuario_service = UsuarioService()