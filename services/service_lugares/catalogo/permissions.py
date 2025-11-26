from rest_framework import permissions

class IsOrganizadorOrAdmin(permissions.BasePermission):
    """
    Permiso personalizado que solo permite acceso a usuarios con rol
    'organizador' o 'admin' (leído desde el Token JWT).
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        try:
            print(f"DEBUG PERMISO: Token payload: {request.auth}") 
            role = request.auth.get('rol')
            return role in ['organizador', 'admin']
        except:
            return False
