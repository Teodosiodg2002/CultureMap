from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Comentario, Voto, Favorito

class InteraccionesAPITests(APITestCase):

    def setUp(self):
        # Datos de prueba
        self.usuario_id_prueba = 1
        self.lugar_id_prueba = 100
        
        # URLs (Nombres actualizados según el refactor)
        self.comentarios_url = reverse('comentario-list-create', kwargs={'lugar_id': self.lugar_id_prueba})
        self.votar_url = reverse('voto-upsert')  # <-- CORREGIDO
        self.favoritos_toggle_url = reverse('favorito-toggle')
        self.favoritos_list_url = reverse('favorito-list')

    # --- TEST COMENTARIOS ---

    def test_get_comentarios_anonimo_exito(self):
        """Un usuario anónimo PUEDE VER los comentarios."""
        response = self.client.get(self.comentarios_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_comentario_anonimo_falla_401(self):
        """Un usuario anónimo NO PUEDE comentar."""
        data = {'texto': 'Comentario anónimo'}
        response = self.client.post(self.comentarios_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_comentario_autenticado_exito(self):
        """Un usuario autenticado PUEDE comentar."""
        self.client.force_authenticate(user=None, token=None) 
        # Simulamos autenticación forzando el request.user
        # Nota: En DRF puro testear auth requiere configurar un usuario real o mockear.
        # Para simplificar y dado que usamos microservicios con tokens simulados:
        
        # Mockeamos la propiedad 'user' en la vista o usamos force_authenticate con un objeto simple
        from django.contrib.auth.models import User
        user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=user)

        data = {'texto': 'Excelente lugar'}
        response = self.client.post(self.comentarios_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comentario.objects.count(), 1)
        self.assertEqual(Comentario.objects.get().usuario_id, user.id)

    # --- TEST VOTOS ---

    def test_post_voto_autenticado_upsert(self):
        """Prueba que el voto se crea y luego se actualiza (Upsert)."""
        from django.contrib.auth.models import User
        user = User.objects.create_user(username='voter', password='password')
        self.client.force_authenticate(user=user)

        # 1. Crear Voto (Upvote)
        data = {'lugar_id': self.lugar_id_prueba, 'valor': 1}
        response = self.client.post(self.votar_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Voto.objects.get(usuario_id=user.id).valor, 1)

        # 2. Actualizar Voto (Downvote) - Misma URL, mismo usuario
        data['valor'] = -1
        response = self.client.post(self.votar_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Voto.objects.get(usuario_id=user.id).valor, -1)

    # --- TEST FAVORITOS ---

    def test_favorito_toggle(self):
        """Prueba dar like y quitar like."""
        from django.contrib.auth.models import User
        user = User.objects.create_user(username='fan', password='password')
        self.client.force_authenticate(user=user)

        data = {'lugar_id': self.lugar_id_prueba}

        # 1. Dar Like (Crear)
        response = self.client.post(self.favoritos_toggle_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Favorito.objects.filter(usuario_id=user.id, lugar_id=self.lugar_id_prueba).exists())

        # 2. Quitar Like (Borrar)
        response = self.client.post(self.favoritos_toggle_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Favorito.objects.filter(usuario_id=user.id, lugar_id=self.lugar_id_prueba).exists())