from django.urls import path
from . import views

urlpatterns = [
   
    path('votar/', views.VotoCreateUpdateView.as_view(), name='voto-crear'),
    path('lugar/<int:lugar_id>/comentarios/', views.ComentarioListCreateView.as_view(), name='comentario-lista-crear'),

    # (Dejamos las rutas de Favoritos pendientes para una futura implementación)
]