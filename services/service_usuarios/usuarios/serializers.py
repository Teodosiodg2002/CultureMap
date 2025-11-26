
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
        username = attrs.get("username")
        password = attrs.get("password")
        
        print(f"🔍 [BACKEND] Validando credenciales para: '{username}'")
        # NO imprimas la contraseña real por seguridad, pero sí su longitud o hash
        print(f"🔍 [BACKEND] Password recibido (longitud): {len(password)}")

        try:
            data = super().validate(attrs)
            print(f"✅ [BACKEND] Validación EXITOSA para {username}")
            return data
        except Exception as e:
            print(f"❌ [BACKEND] Validación FALLIDA para {username}. Razón: {e}")
            raise e
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['rol'] = user.rol
        return token