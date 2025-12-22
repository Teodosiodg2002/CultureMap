from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Comentario, Voto

class InteraccionesAPITests(APITestCase):

    def setUp(self):
        """
        Configura el entorno para cada test.
        Crea un usuario de prueba EN ESTA base de datos.
        """
        self.user = User.objects.create_user(username='testuser', password='password123')

        # 2. ID de lugar de prueba.
        #    No necesitamos un objeto Lugar real, solo su ID (Integer).
        self.lugar_id_prueba = 1

        # 3. URL para la vista de Votos
        self.votar_url = reverse('voto-create')

        # 4. URL para la vista de Comentarios (para el lugar 1)
        self.comentarios_url = reverse('comentario-lista-crear', kwargs={'lugar_id': self.lugar_id_prueba})


    # --- Tests de Comentarios ---

    def test_get_comentarios_anonimo_exito(self):
        """
        PRUEBA: Un usuario anónimo PUEDE VER los comentarios de un lugar.
        (Tu vista 'ComentarioListCreateView' lo permite).
        """
        Comentario.objects.create(
            lugar_id=self.lugar_id_prueba, 
            usuario_id=self.user.id, 
            texto="Comentario de prueba"
        )

        response = self.client.get(self.comentarios_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Comentario de prueba")

    def test_post_comentario_anonimo_falla_401(self):
        """
        PRUEBA: Un usuario anónimo NO PUEDE publicar un comentario.
        """
        data = {"texto": "No debería poder publicar esto"}
        response = self.client.post(self.comentarios_url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_post_comentario_autenticado_exito(self):
        """
        PRUEBA: Un usuario AUTENTICADO PUEDE publicar un comentario.
        """
        self.client.force_authenticate(user=self.user)
        data = {"texto": "¡Este lugar es genial!"}

        response = self.client.post(self.comentarios_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        nuevo_comentario = Comentario.objects.first()
        self.assertEqual(nuevo_comentario.texto, "¡Este lugar es genial!")
        self.assertEqual(nuevo_comentario.usuario_id, self.user.id)
        self.assertEqual(nuevo_comentario.lugar_id, self.lugar_id_prueba)


    # --- Tests de Votos (Lógica de Negocio Real) ---

    def test_post_voto_anonimo_falla_401(self):
        """
        PRUEBA: Un usuario anónimo NO PUEDE votar.
        (Tu vista 'VotoCreateUpdateView' lo prohíbe).
        """
        data = {"lugar_id": self.lugar_id_prueba, "valor": 1}
        response = self.client.post(self.votar_url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_post_voto_autenticado_crea_voto(self):
        """
        PRUEBA: Un usuario AUTENTICADO crea un voto por primera vez (201 CREATED).
        """
        self.client.force_authenticate(user=self.user)
        data = {"lugar_id": self.lugar_id_prueba, "valor": 1}

        response = self.client.post(self.votar_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Voto.objects.count(), 1)
        self.assertEqual(Voto.objects.first().valor, 1)

    def test_post_voto_autenticado_actualiza_voto(self):
        """
        PRUEBA: Un usuario AUTENTICADO que ya ha votado, actualiza su voto (200 OK).
        (Prueba la lógica 'update_or_create' de tu vista).
        """
        Voto.objects.create(
            usuario_id=self.user.id,
            lugar_id=self.lugar_id_prueba,
            valor=1
        )
        self.assertEqual(Voto.objects.count(), 1)

        self.client.force_authenticate(user=self.user)

        data = {"lugar_id": self.lugar_id_prueba, "valor": -1}
        response = self.client.post(self.votar_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Voto.objects.count(), 1)
        self.assertEqual(Voto.objects.first().valor, -1)