from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_lugares, name="index_lugares"),
    path("<int:pk>/", views.detalle_lugar, name="detalle_lugar"),
    path('eventos/', views.index_eventos, name='index_eventos'),
    
    path("crear/", views.seleccionar_creacion, name="seleccionar_creacion"),
    path("crear/lugar/", views.crear_lugar, name="crear_lugar"),
    path("crear/evento/", views.crear_evento, name="crear_evento"),
    
    path("dashboard/", views.dashboard, name="dashboard"),
    path("borrar/<str:tipo>/<int:pk>/", views.borrar_recurso, name="borrar_recurso"),
    path("cambiar-rol/<int:pk>/", views.cambiar_rol, name="cambiar_rol"),
    
    path("gestionar/<str:tipo>/<int:pk>/<str:accion>/", views.gestionar_recurso, name="gestionar_recurso"),
    
]