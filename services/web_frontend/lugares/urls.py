from django.urls import path
from . import views

urlpatterns = [
    # ... (Rutas Index y Login se mantienen igual) ...
    path("", views.index_lugares, name="index_lugares"),
    path("eventos/", views.index_eventos, name="index_eventos"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # ... Rutas de creación/borrado ...
    path("crear/", views.seleccionar_creacion, name="seleccionar_creacion"),
    path("crear/lugar/", views.crear_lugar, name="crear_lugar"),
    path("crear/evento/", views.crear_evento, name="crear_evento"),
    path("borrar/<str:tipo>/<int:pk>/", views.borrar_recurso, name="borrar_recurso"),
    path("cambiar-rol/<int:pk>/", views.cambiar_rol, name="cambiar_rol"),
    path("gestionar/<str:tipo>/<int:pk>/<str:accion>/", views.gestionar_recurso, name="gestionar_recurso"),

    # DETALLES
    path("lugar/<int:pk>/", views.detalle_lugar, name="detalle_lugar"), # Antes era solo <int:pk>/
    path("evento/<int:pk>/", views.detalle_evento, name="detalle_evento"),

    # INTERACCIONES (Ahora aceptan 'tipo')
    path("favorito/<str:tipo>/<int:pk>/", views.accion_favorito, name="accion_favorito"),
    path("votar/<str:tipo>/<int:pk>/<int:valor>/", views.accion_votar, name="accion_votar"),
    
    #RANKING Y PERFILES PÚBLICOS
    path("ranking/", views.ver_ranking, name="ver_ranking"),
    path("perfil/<int:pk>/", views.ver_perfil, name="ver_perfil"),
]