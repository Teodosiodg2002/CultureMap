from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_lugares, name="index_lugares"),
    path("<int:pk>/", views.detalle_lugar, name="detalle_lugar"),
    path("crear/", views.crear_lugar, name="crear_lugar"),
]
