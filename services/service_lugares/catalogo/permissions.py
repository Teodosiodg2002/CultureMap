from rest_framework import permissions

class IsOrganizadorOrAdmin(permissions.BasePermission):
    """
    Permiso personalizado que solo permite acceso a usuarios con rol
    'organizador' o 'admin' (leído desde el Token JWT).
    """

    def has_permission(self, request, view):
        # 1. Verificar si el usuario está autenticado
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. Leer el rol desde el token (request.auth es el payload del token decodificado)
        try:
            user_rol = request.auth.get('rol', None)
        except AttributeError:
            return False

        return user_rol in ['organizador', 'admin']