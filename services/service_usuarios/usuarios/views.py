from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    """
    Vista de API para crear (registrar) un nuevo usuario.
    """
    queryset = User.objects.all()
    # 'permissions.AllowAny' permite que cualquiera (incluso anónimos)
    # pueda acceder a esta vista para registrarse.
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer