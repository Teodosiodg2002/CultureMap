from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import IsAdmin
from .serializers import (
    UserRegistrationSerializer, 
    MyTokenObtainPairSerializer, 
    UserManagementSerializer,
    PublicProfileSerializer
)

User = get_user_model()

# --- AUTENTICACIÓN Y REGISTRO ---

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    """Vista para administradores: gestión completa de usuarios"""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserManagementSerializer
    permission_classes = [IsAdmin]

# --- GAMIFICACIÓN Y PERFIL ---

class MeView(APIView):
    """Devuelve los datos del usuario logueado actual"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserManagementSerializer(request.user)
        return Response(serializer.data)

class PublicProfileView(generics.RetrieveAPIView):
    """Ver el perfil público de cualquier usuario"""
    queryset = User.objects.filter(is_active=True)
    serializer_class = PublicProfileSerializer
    permission_classes = [permissions.AllowAny]

class RankingView(generics.ListAPIView):
    """Top 10 usuarios con más puntos"""
    queryset = User.objects.filter(is_active=True).order_by('-puntos')[:10]
    serializer_class = PublicProfileSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['PATCH', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def sumar_puntos(request, pk):
    """Endpoint para sumar puntos a un usuario (llamado por el frontend tras acción)"""
    try:
        user = User.objects.get(pk=pk)
        
        # En un entorno real, validaríamos que request.user es un servicio o tiene permisos.
        # Por ahora permitimos que el usuario logueado sume puntos (lógica frontend-driven).
        
        puntos_extra = int(request.data.get('puntos', 0))
        if puntos_extra > 0:
            user.puntos += puntos_extra
            user.save()
            
        return Response({
            'mensaje': f'Se han sumado {puntos_extra} puntos.',
            'total_puntos': user.puntos,
            'nivel': user.nivel
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({'error': 'El valor de puntos debe ser un número'}, status=status.HTTP_400_BAD_REQUEST)