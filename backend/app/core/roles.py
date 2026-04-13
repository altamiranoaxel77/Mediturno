# =============================================================================
# app/core/roles.py — Constantes de roles del sistema
# =============================================================================
# Centralizar los nombres de roles evita usar "magic strings" en el código.
# En lugar de escribir if rol == "Admin" en cada archivo, importamos la constante.
# Si el nombre cambia, se cambia en un solo lugar.
# =============================================================================

class Roles:
    SUPERADMIN = "SuperAdmin"
    ADMIN      = "Admin"
    SECRETARIO = "Secretario"
    DOCTOR     = "Doctor"