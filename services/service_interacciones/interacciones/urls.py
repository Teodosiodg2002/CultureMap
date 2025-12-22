from django.urls import path
from .views import ComentarioListCreateView, VotoCreateUpdateView


urlpatterns = [
    path('comentarios/<int:lugar_id>/', ComentarioListCreateView.as_view(), name='comentario-list-create'),
    path('votos/', VotoCreateUpdateView.as_view(), name='voto-create'),
]