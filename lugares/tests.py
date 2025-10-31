# lugares/tests.py

from django.test import TestCase
from django.urls import reverse
from .models import Categoria, Lugar, EstadoAprobacion
from django.contrib.auth.models import User


# Los tests se agrupan en clases. Esta clase probará nuestro modelo Lugar.
class LugarModelTests(TestCase):

    def test_propiedad_es_visible(self):
        """
        Este test comprueba que la propiedad 'es_visible' de nuestro modelo
        funciona como esperamos.
        """
        # ARRANGE: Preparamos el escenario. Creamos dos lugares.
        lugar_que_debe_ser_visible = Lugar.objects.create(
            nombre="Lugar Aprobado", estado=EstadoAprobacion.APROBADO, publicado=True
        )

        lugar_que_NO_debe_ser_visible = Lugar.objects.create(
            nombre="Lugar Pendiente", estado=EstadoAprobacion.PENDIENTE, publicado=True
        )

        # ACT & ASSERT: Actuamos y comprobamos.
        # Comprobamos que el primer lugar devuelve True.
        self.assertTrue(lugar_que_debe_ser_visible.es_visible)

        # Comprobamos que el segundo lugar devuelve False.
        self.assertFalse(lugar_que_NO_debe_ser_visible.es_visible)


class LugarViewTests(TestCase):

    def setUp(self):
        """
        setUp es un método especial que se ejecuta ANTES de cada test.
        Lo usamos para crear datos de prueba que usaremos en varios tests.
        """
        self.lugar_aprobado = Lugar.objects.create(
            nombre="Lugar Aprobado de Prueba",
            estado=EstadoAprobacion.APROBADO,
            publicado=True,
        )
        self.lugar_pendiente = Lugar.objects.create(
            nombre="Lugar Pendiente de Prueba",
            estado=EstadoAprobacion.PENDIENTE,
            publicado=True,
        )
        self.test_user = User.objects.create_user(
            username="testuser", password="password123"
        )

    # en lugares/tests.py, dentro de LugarViewTests

    def test_vista_index_lugares_funciona(self):
        """
        Prueba que la página de la lista de lugares (index) carga
        correctamente y solo muestra los lugares aprobados.
        """
        url = reverse("index_lugares")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.lugar_aprobado.nombre)
        self.assertNotContains(response, self.lugar_pendiente.nombre)

    def test_vista_detalle_funciona_para_lugar_aprobado(self):
        """
        Prueba que la página de detalle de un lugar APROBADO carga bien.
        """
        url = reverse("detalle_lugar", args=[self.lugar_aprobado.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.lugar_aprobado.nombre)

    def test_vista_detalle_da_404_para_lugar_pendiente(self):
        """
        Prueba que la página de detalle de un lugar PENDIENTE
        devuelve un error 404 (No Encontrado).
        """
        url = reverse("detalle_lugar", args=[self.lugar_pendiente.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)  # 404 = No Encontrado

    def test_login_post_redirects_to_index(self):
        """
        Prueba que un POST exitoso al login redirige a la página principal.
        Esto simula a un usuario enviando el formulario.
        """
        credentials = {
            'username': 'testuser',
            'password': 'password123'
        }

        # Simulamos un 'POST' a la URL de login con esas credenciales
        response = self.client.post(reverse('login'), credentials)

        self.assertRedirects(response, reverse('index_lugares'))

    def test_protected_view_redirects_to_login(self):
        """
        Prueba que un usuario no logueado es redirigido al login
        al intentar acceder a 'crear_lugar'.
        """
        # Intentamos acceder a 'crear_lugar' SIN estar logueados
        response = self.client.get(reverse("crear_lugar"))

        # Comprobamos que nos redirige a la página de login
        login_url = reverse("login")
        crear_url = reverse("crear_lugar")
        self.assertRedirects(response, f"{login_url}?next={crear_url}")

    def test_crear_lugar_get_authenticated_user(self):
        """
        Prueba que un usuario logueado PUEDE ver la página del formulario.
        """
        self.client.login(username='testuser', password='password123')

        response = self.client.get(reverse('crear_lugar'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lugares/crear_lugar.html')

    def test_crear_lugar_post_authenticated_user(self):
        """
        Prueba que un usuario logueado PUEDE enviar un nuevo lugar.
        """
        self.client.login(username='testuser', password='password123')

        lugar_count_before = Lugar.objects.count()

        lugar_data = {
            'nombre': 'Lugar de Test desde POST',
            'descripcion': 'Descripción de prueba.',
            'categoria': Categoria.OTROS,
            'lat': 40.0,
            'lng': -3.0
        }

        response = self.client.post(reverse('crear_lugar'), lugar_data)

        lugar_count_after = Lugar.objects.count()

        self.assertEqual(lugar_count_after, lugar_count_before + 1)

        nuevo_lugar = Lugar.objects.latest('creado_en')
        self.assertEqual(nuevo_lugar.nombre, 'Lugar de Test desde POST')
        self.assertEqual(nuevo_lugar.creado_por, self.test_user)
        self.assertEqual(nuevo_lugar.estado, EstadoAprobacion.PENDIENTE)

        # Verificamos que nos redirige a la página principal (index)
        self.assertRedirects(response, reverse('index_lugares'))