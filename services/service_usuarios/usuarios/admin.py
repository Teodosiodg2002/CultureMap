from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
class CustomUserAdmin(UserAdmin):
    # Añadimos tus campos personalizados al formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Información Extra de CultureMap', {'fields': ('rol', 'biografia', 'puntos')}),
    )
    
    # Columnas que se verán en la lista de usuarios
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'puntos', 'is_staff')
    
    # Filtros laterales
    list_filter = UserAdmin.list_filter + ('rol',)

# Registramos solo el Usuario con la configuración personalizada
admin.site.register(Usuario, CustomUserAdmin)