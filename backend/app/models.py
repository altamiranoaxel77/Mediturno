# =============================================================================
# app/models.py — Importación centralizada de todos los modelos
# =============================================================================
# SQLAlchemy necesita que todos los modelos estén cargados en memoria
# para poder resolver las relaciones entre ellos.
#
# IMPORTANTE: respetar el orden — primero los modelos sin FK,
# después los que dependen de otros.
# =============================================================================

from app.modules.rol.model            import Rol               # noqa: F401
from app.modules.hospital.model       import Hospital          # noqa: F401
from app.modules.especialidad.model   import Especialidad      # noqa: F401
from app.modules.obra_social.model    import ObraSocial        # noqa: F401
from app.modules.dia_semana.model     import DiaSemana         # noqa: F401
from app.modules.usuario.model        import Usuario           # noqa: F401
from app.modules.medico.model         import Medico            # noqa: F401
from app.modules.paciente.model       import Paciente          # noqa: F401
from app.modules.disponibilidad.model import DisponibilidadMedico  # noqa: F401
from app.modules.turno.model          import Turno             # noqa: F401