# lugares/tests.py

from django.test import TestCase
from django.urls import reverse
from .models import Lugar, EstadoAprobacion

# Los tests se agrupan en clases. Esta clase probará nuestro modelo Lugar.
class LugarModelTests(TestCase):

    def test_propiedad_es_visible(self):
        """
        Este test comprueba que la propiedad 'es_visible' de nuestro modelo
        funciona como esperamos.
        """
        # ARRANGE: Preparamos el escenario. Creamos dos lugares.
        lugar_que_debe_ser_visible = Lugar.objects.create(
            nombre="Lugar Aprobado",
            estado=EstadoAprobacion.APROBADO,
            publicado=True
        )

        lugar_que_NO_debe_ser_visible = Lugar.objects.create(
            nombre="Lugar Pendiente",
            estado=EstadoAprobacion.PENDIENTE,
            publicado=True
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
            publicado=True
        )
        self.lugar_pendiente = Lugar.objects.create(
            nombre="Lugar Pendiente de Prueba",
            estado=EstadoAprobacion.PENDIENTE,
            publicado=True
        )

    def test_vista_lista_aprobados_funciona(self):
        """
        Prueba que la página de la lista de lugares aprobados carga
        correctamente y solo muestra los lugares aprobados.
        """
        # Obtenemos la URL usando su nombre de 'urls.py'
        url = reverse('listar_lugares_aprobados')
        
        # self.client es un navegador web falso para hacer peticiones
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200) # 200 = OK
        self.assertContains(response, self.lugar_aprobado.nombre)
        self.assertNotContains(response, self.lugar_pendiente.nombre)

    def test_vista_detalle_funciona_para_lugar_aprobado(self):
        """
        Prueba que la página de detalle de un lugar APROBADO carga bien.
        """
        url = reverse('detalle_lugar', args=[self.lugar_aprobado.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.lugar_aprobado.nombre)

    def test_vista_detalle_da_404_para_lugar_pendiente(self):
        """
        Prueba que la página de detalle de un lugar PENDIENTE
        devuelve un error 404 (No Encontrado).
        """
        url = reverse('detalle_lugar', args=[self.lugar_pendiente.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404) # 404 = No Encontrado