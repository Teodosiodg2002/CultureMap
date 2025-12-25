from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, label="Confirmar contraseña")

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'rol')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        return User.objects.create_user(**validated_data, is_active=True)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['rol'] = user.rol
        token['id'] = user.id  # Incluimos el ID en el token también por utilidad
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['rol'] = self.user.rol
        data['id'] = self.user.id
        return data

class UserManagementSerializer(serializers.ModelSerializer):
    """Serializer completo para administración o perfil propio"""
    nivel = serializers.ReadOnlyField() # Campo calculado

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'rol', 'is_active', 'date_joined', 'biografia', 'puntos', 'nivel')
        read_only_fields = ('username', 'email', 'date_joined', 'puntos', 'nivel')

class PublicProfileSerializer(serializers.ModelSerializer):
    """Serializer seguro para ver perfiles de OTROS usuarios (sin email ni datos sensibles)"""
    nivel = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'username', 'rol', 'biografia', 'puntos', 'nivel', 'date_joined')