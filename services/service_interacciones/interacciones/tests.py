from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Comentario, Voto, Favorito

class InteraccionesAPITests(APITestCase):

    def setUp(self):
        # Datos de prueba
        self.usuario_id_prueba = 1
        self.lugar_id_prueba = 100
        self.evento_id_prueba = 200
        
        # URLs Actualizadas (Segun el nuevo urls.py)
        self.comentarios_lugar_url = reverse('comentario-lugar', kwargs={'lugar_id': self.lugar_id_prueba})
        self.comentarios_evento_url = reverse('comentario-evento', kwargs={'evento_id': self.evento_id_prueba})
        
        self.votar_url = reverse('voto-upsert')
        self.favoritos_toggle_url = reverse('favorito-toggle')
        self.mis_votos_url = reverse('mis-votos')

    # --- TEST COMENTARIOS ---

    def test_get_comentarios_lugar_exito(self):
        """Un usuario anónimo PUEDE VER los comentarios de un lugar."""
        response = self.client.get(self.comentarios_lugar_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_comentario_anonimo_falla(self):
        """Un usuario anónimo NO PUEDE comentar."""
        data = {'texto': 'Comentario anónimo'}
        response = self.client.post(self.comentarios_lugar_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_comentario_lugar_autenticado(self):
        """Un usuario autenticado PUEDE comentar en un lugar."""
        from django.contrib.auth.models import User
        user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=user)

        data = {'texto': 'Excelente lugar'}
        response = self.client.post(self.comentarios_lugar_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comentario.objects.count(), 1)
        self.assertEqual(Comentario.objects.first().lugar_id, self.lugar_id_prueba)

    def test_post_comentario_evento_autenticado(self):
        """Un usuario autenticado PUEDE comentar en un evento (Polimorfismo)."""
        from django.contrib.auth.models import User
        user = User.objects.create_user(username='eventfan', password='password')
        self.client.force_authenticate(user=user)

        data = {'texto': 'Me encanta este evento'}
        response = self.client.post(self.comentarios_evento_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comentario.objects.count(), 1)
        self.assertEqual(Comentario.objects.first().evento_id, self.evento_id_prueba)

    # --- TEST VOTOS (ESTRELLAS 1-5) ---

    def test_post_voto_lugar_upsert(self):
        """Prueba votar un lugar con estrellas (1-5) y actualizarlo."""
        from django.contrib.auth.models import User
        user = User.objects.create_user(username='voter', password='password')
        self.client.force_authenticate(user=user)

        # 1. Crear Voto (5 Estrellas)
        data = {'lugar_id': self.lugar_id_prueba, 'valor': 5}
        response = self.client.post(self.votar_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Voto.objects.get(usuario_id=user.id).valor, 5)

        # 2. Actualizar Voto (Bajada a 3 Estrellas) - Upsert
        data['valor'] = 3
        response = self.client.post(self.votar_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Voto.objects.get(usuario_id=user.id).valor, 3)

    def test_post_voto_invalido(self):
        """El voto debe ser entre 1 y 5."""
        from django.contrib.auth.models import User
        user = User.objects.create_user(username='hacker', password='password')
        self.client.force_authenticate(user=user)

        data = {'lugar_id': self.lugar_id_prueba, 'valor': 10} # Inválido
        response = self.client.post(self.votar_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- TEST FAVORITOS ---

    def test_favorito_toggle_evento(self):
        """Prueba dar like y quitar like a un evento."""
        from django.contrib.auth.models import User
        user = User.objects.create_user(username='fan', password='password')
        self.client.force_authenticate(user=user)

        data = {'evento_id': self.evento_id_prueba}

        # 1. Dar Like (Crear)
        response = self.client.post(self.favoritos_toggle_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Favorito.objects.filter(usuario_id=user.id, evento_id=self.evento_id_prueba).exists())

        # 2. Quitar Like (Borrar)
        response = self.client.post(self.favoritos_toggle_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Favorito.objects.filter(usuario_id=user.id, evento_id=self.evento_id_prueba).exists())