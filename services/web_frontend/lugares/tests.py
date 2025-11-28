# lugares/tests.py

from django.test import TestCase
from django.urls import reverse
from .models import Categoria, Lugar, EstadoAprobacion
from django.contrib.auth.models import User

from django.test import TestCase

# Los tests antiguos de modelos se han movido a los microservicios.
class FrontendTests(TestCase):
    def test_dummy(self):
        self.assertTrue(True)