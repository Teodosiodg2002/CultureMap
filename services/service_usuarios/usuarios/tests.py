from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class UsuarioAPITests(APITestCase):

    def setUp(self):
        """
        Define las URLs que usaremos en los tests.
        """
        self.register_url = reverse('user-register')
        self.token_url = reverse('token_obtain_pair')

        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password123'
        }

        self.login_data = {
            'username': 'testuser',
            'password': 'password123'
        }


    # --- Tests de Registro (POST /api/register/) ---

    def test_registro_exitoso(self):
        """
        PRUEBA: Un usuario puede registrarse con éxito.
        """
        response = self.client.post(self.register_url, self.user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_registro_password_no_coincide(self):
        """
        PRUEBA: El registro falla si 'password' y 'password2' no coinciden.
        """
        data = self.user_data.copy()
        data['password2'] = 'passwordDISTINTA'

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('password', response.data)

        self.assertEqual(User.objects.count(), 0)

    def test_registro_usuario_ya_existe(self):
        """
        PRUEBA: El registro falla si el usuario ya existe.
        """
        self.client.post(self.register_url, self.user_data, format='json')

        response = self.client.post(self.register_url, self.user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(User.objects.count(), 1) # Sigue habiendo solo 1 usuario


    # --- Tests de Login (POST /api/token/) ---

    def test_login_exitoso_obtiene_token(self):
        """
        PRUEBA: Un usuario registrado puede hacer login y obtener tokens.
        """
        self.client.post(self.register_url, self.user_data, format='json')

        response = self.client.post(self.token_url, self.login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_password_incorrecta_falla_401(self):
        """
        PRUEBA: El login falla si la contraseña es incorrecta.
        """
        self.client.post(self.register_url, self.user_data, format='json')

        login_data_mal = self.login_data.copy()
        login_data_mal['password'] = 'contraseñaincorrecta'

        response = self.client.post(self.token_url, login_data_mal, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)