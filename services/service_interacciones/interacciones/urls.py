from django.urls import path
from .views import (
    ComentarioListCreateView, 
    VotoUpsertView, 
    FavoritoToggleView, 
    FavoritoListView
)

urlpatterns = [
    # Comentarios (vinculados a un lugar en la URL)
    path('comentarios/<int:lugar_id>/', ComentarioListCreateView.as_view(), name='comentario-list-create'),
    
    # Votos
    path('votar/', VotoUpsertView.as_view(), name='voto-upsert'),
    
    # Favoritos
    path('favoritos/', FavoritoListView.as_view(), name='favorito-list'),
    path('favoritos/toggle/', FavoritoToggleView.as_view(), name='favorito-toggle'),
]