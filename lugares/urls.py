from django.urls import path
from . import views

urlpatterns = [
    path('',views.listar_lugares_todos, name='listar_lugares_todos'),
    path('aprobados/',views.listar_lugares_aprobados, name='listar_lugares_aprobados'),
    path('<int:pk>/',views.detalle_lugar, name='detalle_lugar'),
]
