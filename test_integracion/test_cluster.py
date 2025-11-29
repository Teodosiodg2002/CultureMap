import unittest
import requests
import uuid
import os
from dotenv import load_dotenv

load_dotenv('.env.test')

class CultureMapIntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Carga configuración y verifica requisitos previos"""
        cls.api_usuarios = os.getenv("API_USUARIOS", "http://localhost:8001/api")
        cls.api_lugares = os.getenv("API_LUGARES", "http://localhost:8002/api/catalogo")
        
        cls.admin_user = os.getenv("TEST_ADMIN_USER")
        cls.admin_pass = os.getenv("TEST_ADMIN_PASS")

        if not cls.admin_user or not cls.admin_pass:
            print("\n No hay credenciales de ADMIN en .env.test.")

    def setUp(self):
        """Datos aleatorios para cada test"""
        self.suffix = str(uuid.uuid4())[:8]
        self.username = f"user_{self.suffix}"
        self.password = "TestPass_123"
        self.email = f"test_{self.suffix}@culturemap.com"

    def _get_headers(self, token):
        return {'Authorization': f'Bearer {token}'}

    def _registrar_y_login(self, rol="usuario"):
        """Helper: Registra usuario y devuelve token"""
        # 1. Registro
        payload = {
            "username": self.username, "email": self.email,
            "password": self.password, "password2": self.password,
            "rol": rol
        }
        requests.post(f"{self.api_usuarios}/register/", json=payload)

        # 2. Login
        res = requests.post(f"{self.api_usuarios}/token/", json={
            "username": self.username, "password": self.password
        })
        
        if res.status_code != 200:
            self.fail(f"Fallo Login ({rol}): {res.text}")
            
        return res.json()['access']

    def _obtener_token_admin(self):
        """Helper: Obtiene token del admin configurado"""
        if not self.admin_user or not self.admin_pass:
            self.skipTest("Se requieren credenciales de Admin")

        res = requests.post(f"{self.api_usuarios}/token/", json={
            "username": self.admin_user, "password": self.admin_pass
        })
        
        if res.status_code != 200:
            self.fail("Error autenticando al Admin. Revisa .env.test")
            
        return res.json()['access']

    # --- TESTS ---

    def test_flujo_completo_lugar(self):
        """Prueba: Crear lugar (Org) -> Aprobar (Admin) -> Ver (Público)"""
        print(f"\n[TEST] Ciclo de vida de un Lugar ({self.suffix})")

        # 1. Organizador crea lugar
        token_org = self._registrar_y_login(rol="organizador")
        datos_lugar = {
            "nombre": f"Lugar Test {self.suffix}",
            "descripcion": "Test integración",
            "lat": 37.18, "lng": -3.60, "categoria": "bar"
        }
        res_crear = requests.post(f"{self.api_lugares}/lugares/", json=datos_lugar, 
                                  headers=self._get_headers(token_org))
        self.assertEqual(res_crear.status_code, 201)
        lugar_id = res_crear.json()['id']

        # 2. Admin aprueba
        token_admin = self._obtener_token_admin()
        res_aprobar = requests.put(f"{self.api_lugares}/lugares/{lugar_id}/aprobar/", 
                                   headers=self._get_headers(token_admin))
        self.assertEqual(res_aprobar.status_code, 200)

        # 3. Verificar público
        res_publico = requests.get(f"{self.api_lugares}/lugares/{lugar_id}/")
        self.assertEqual(res_publico.status_code, 200)
        self.assertEqual(res_publico.json()['estado'], 'aprobado')
        print("Flujo correcto.")

    def test_seguridad_roles(self):
        """Prueba: Un usuario normal NO debe poder aprobar"""
        print(f"\n[TEST] Verificación de Seguridad")

        token_org = self._registrar_y_login(rol="organizador")
        res = requests.post(f"{self.api_lugares}/lugares/", json={
            "nombre": "Intento Hack", "descripcion": "...", "lat": 0, "lng": 0, "categoria": "otros"
        }, headers=self._get_headers(token_org))
        lugar_id = res.json()['id']

        self.username = f"normal_{self.suffix}"
        token_normal = self._registrar_y_login(rol="usuario")
        
        res_hack = requests.put(f"{self.api_lugares}/lugares/{lugar_id}/aprobar/", 
                                headers=self._get_headers(token_normal))

        # 3. Validar que falla
        self.assertEqual(res_hack.status_code, 403)
        print("Seguridad correcta (403 recibido).")

if __name__ == '__main__':
    unittest.main()