from django.urls import path
from .views import (
    ComentarioListCreateView, 
    VotoUpsertView, 
    FavoritoToggleView, 
    FavoritoListView,
    VotoListView,     
    VotoResumenView    
)

urlpatterns = [
    # Comentarios
    path('comentarios/lugar/<int:lugar_id>/', ComentarioListCreateView.as_view(), name='comentario-lugar'),
    path('comentarios/evento/<int:evento_id>/', ComentarioListCreateView.as_view(), name='comentario-evento'),
    
    # Acciones
    path('votar/', VotoUpsertView.as_view(), name='voto-upsert'),
    path('favoritos/', FavoritoListView.as_view(), name='favorito-list'),
    path('favoritos/toggle/', FavoritoToggleView.as_view(), name='favorito-toggle'),

    # Consultas de Datos
    path('mis-votos/', VotoListView.as_view(), name='mis-votos'),
    path('votos/resumen/<str:tipo>/<int:pk>/', VotoResumenView.as_view(), name='voto-resumen'),
]