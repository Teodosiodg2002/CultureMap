from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User

class StatelessJWTAuthentication(JWTAuthentication):
    """
    Autenticación JWT que NO comprueba la base de datos local.
    Confía en el contenido del token para crear un usuario temporal.
    """
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
        except KeyError:
            return None

        # Creamos un usuario en memoria (no se guarda en BBDD)
        user = User()
        user.id = user_id
        user.username = validated_token.get('username', 'usuario_token')
        user.rol = validated_token.get('rol', 'usuario')
        return user