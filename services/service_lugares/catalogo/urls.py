from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LugarViewSet

router = DefaultRouter()

router.register(r'lugares', LugarViewSet, basename='lugar')

urlpatterns = [
    path('', include(router.urls)),
]