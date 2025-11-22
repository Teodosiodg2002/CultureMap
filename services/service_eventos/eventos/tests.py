from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Evento, EstadoEvento, CategoriaEvento
from django.utils import timezone

class EventoAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

        self.evento = Evento.objects.create(
            nombre="Concierto Test",
            descripcion="Un concierto de prueba",
            fecha_inicio=timezone.now(),
            lat=37.1, lng=-3.1,
            categoria=CategoriaEvento.CONCIERTO,
            estado=EstadoEvento.PUBLICADO,
            creado_por_id=self.user.id
        )

        self.list_url = reverse('evento-list')

    def test_get_eventos_publicos(self):
        """Cualquiera puede ver la lista de eventos"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Concierto Test")

    def test_post_crear_evento_autenticado(self):
        """Un usuario autenticado puede proponer un evento"""
        self.client.force_authenticate(user=self.user)

        data = {
            "nombre": "Nuevo Evento",
            "descripcion": "Descripción",
            "fecha_inicio": timezone.now(),
            "lat": 37.2, "lng": -3.2,
            "categoria": "teatro"
        }

        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Evento.objects.count(), 2)

        nuevo = Evento.objects.latest('creado_en')
        self.assertEqual(nuevo.estado, EstadoEvento.PENDIENTE)
        # Nota: Si en la vista pusiste 'creado_por_id=1' fijo, esto será 1.
        # Si pusiste self.request.user.id, será self.user.id.