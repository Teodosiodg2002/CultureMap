from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView, 
    MyTokenObtainPairView,  
    UserViewSet, 
    MeView, 
    PublicProfileView, 
    RankingView, 
    sumar_puntos
)

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # Autenticación
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Perfil Propio
    path('me/', MeView.as_view(), name='user-me'),

    # Gamificación
    path('ranking/', RankingView.as_view(), name='ranking'),
    path('<int:pk>/perfil/', PublicProfileView.as_view(), name='public-profile'),
    path('<int:pk>/puntos/', sumar_puntos, name='sumar-puntos'),

    # Rutas del Router (Admin)
    path('', include(router.urls)),
]