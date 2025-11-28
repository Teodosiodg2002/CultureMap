from rest_framework import permissions

class IsOrganizadorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Leemos el atributo 'rol' que nuestro Authentication inyectó
        rol = getattr(request.user, 'rol', None)
        return rol in ['organizador', 'admin']