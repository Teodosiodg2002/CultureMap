
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
        # Validamos que coincidan
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
            if 'password2' in validated_data:
                validated_data.pop('password2')
            
            user = User.objects.create_user(**validated_data)
            
            user.is_active = True
            user.save()
            
            return user

# --- Serializador de Token (Para incluir el Rol) ---
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['rol'] = self.user.rol
        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['rol'] = user.rol
        return token
    
class UserManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'rol', 'is_active', 'date_joined')
        read_only_fields = ('username', 'email', 'date_joined')