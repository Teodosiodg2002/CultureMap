from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'rol', None) == 'admin'
    
class IsOrganizadorOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        rol = getattr(request.user, 'rol', None)
        return rol in ['organizador', 'admin']