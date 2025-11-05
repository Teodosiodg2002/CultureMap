# services/service_lugares/catalogo/tests.py

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Lugar, EstadoAprobacion, Categoria

class LugarAPITests(APITestCase):

    def setUp(self):
        """
        Configura el entorno para cada test.
        Crea un usuario y lugares de prueba EN ESTA base de datos.
        """
        self.user = User.objects.create_user(username='testuser', password='password123')

        self.lugar_aprobado = Lugar.objects.create(
            nombre="Lugar Aprobado de Prueba",
            descripcion="Este sí es visible.",
            lat=37.1, lng=-3.1,
            categoria=Categoria.MIRADOR,
            estado=EstadoAprobacion.APROBADO,
            publicado=True,
            creado_por_id=self.user.id
        )

        self.lugar_pendiente = Lugar.objects.create(
            nombre="Lugar Pendiente de Prueba",
            descripcion="Este no es visible.",
            lat=37.2, lng=-3.2,
            categoria=Categoria.BAR,
            estado=EstadoAprobacion.PENDIENTE,
            publicado=True,
            creado_por_id=self.user.id
        )

        self.list_create_url = reverse('lugar-list')


    # --- Tests de LECTURA (GET) ---

    def test_get_lista_lugares_anonimo(self):
        """
        PRUEBA: Un usuario anónimo PUEDE VER la lista de lugares (solo los aprobados).
        (Equivalente a tu prueba GET en el navegador).
        """
        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.lugar_aprobado.nombre)
        self.assertNotContains(response, self.lugar_pendiente.nombre)

    def test_get_detalle_lugar_anonimo(self):
        """
        PRUEBA: Un usuario anónimo PUEDE VER el detalle de un lugar APROBADO.
        """
        url = reverse('lugar-detail', kwargs={'pk': self.lugar_aprobado.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], self.lugar_aprobado.nombre)

    def test_get_detalle_lugar_pendiente_falla_404(self):
        """
        PRUEBA: Un usuario anónimo NO PUEDE VER el detalle de un lugar PENDIENTE.
        (Tu ViewSet lo filtra, por lo que debe dar 404).
        """
        url = reverse('lugar-detail', kwargs={'pk': self.lugar_pendiente.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # --- Tests de ESCRITURA (POST) ---

    def test_post_crear_lugar_anonimo_falla_401(self):
        """
        PRUEBA: Un usuario anónimo NO PUEDE CREAR un lugar.
        (Tu permiso 'IsAuthenticatedOrReadOnly' debe bloquearlo).
        """
        data = {"nombre": "Lugar Anónimo", "categoria": "otros", "lat": 1.0, "lng": 1.0}
        response = self.client.post(self.list_create_url, data, format='json')

        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_post_crear_lugar_autenticado_exito(self):
        """
        PRUEBA: Un usuario AUTENTICADO PUEDE CREAR un lugar.
        (Equivalente a tu prueba POST con Postman).
        """
        self.client.force_authenticate(user=self.user)

        data = {
            "nombre": "Lugar de Test Autenticado",
            "descripcion": "Descripción de prueba.",
            "lat": 37.3,
            "lng": -3.3,
            "categoria": "mirador"
        }

        # 2. Enviamos el POST con los datos en formato 'json'
        response = self.client.post(self.list_create_url, data, format='json')

        # 3. Comprobamos el éxito
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 4. Comprobamos que la lógica de 'perform_create' funcionó
        nuevo_lugar = Lugar.objects.get(nombre="Lugar de Test Autenticado")
        self.assertEqual(nuevo_lugar.creado_por_id, self.user.id)
        self.assertEqual(nuevo_lugar.estado, EstadoAprobacion.PENDIENTE)