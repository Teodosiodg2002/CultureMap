from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),  # ruta principal de la app
]
