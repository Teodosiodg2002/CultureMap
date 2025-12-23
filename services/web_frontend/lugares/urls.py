from django.urls import path
from . import views

urlpatterns = [
    # ... tus rutas anteriores ...
    path("", views.index_lugares, name="index_lugares"),
    path("eventos/", views.index_eventos, name="index_eventos"),
    path("<int:pk>/", views.detalle_lugar, name="detalle_lugar"),

    # ... rutas de auth y dashboard ...
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    
    # ... rutas de creación/borrado ...
    path("crear/", views.seleccionar_creacion, name="seleccionar_creacion"),
    path("crear/lugar/", views.crear_lugar, name="crear_lugar"),
    path("crear/evento/", views.crear_evento, name="crear_evento"),
    path("borrar/<str:tipo>/<int:pk>/", views.borrar_recurso, name="borrar_recurso"),
    path("cambiar-rol/<int:pk>/", views.cambiar_rol, name="cambiar_rol"),
    path("gestionar/<str:tipo>/<int:pk>/<str:accion>/", views.gestionar_recurso, name="gestionar_recurso"),

    # --- Rutas para las interacciones ---
    path("favorito/<int:pk>/", views.accion_favorito, name="accion_favorito"),
    path("votar/<int:pk>/<str:valor>/", views.accion_votar, name="accion_votar"),
]