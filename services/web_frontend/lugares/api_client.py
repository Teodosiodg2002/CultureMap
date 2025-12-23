import requests
from django.conf import settings

class ApiClient:
    """Cliente centralizado para comunicar con los microservicios."""
    
    @staticmethod
    def _get_headers(token=None):
        return {'Authorization': f'Bearer {token}'} if token else {}

    @staticmethod
    def _process_response(response):
        """Procesa la respuesta JSON manejando paginación automáticamente."""
        if response.status_code in [200, 201]:
            try:
                data = response.json()
                # Si es un diccionario con 'results', es paginación: devolvemos la lista
                if isinstance(data, dict) and 'results' in data:
                    return data['results']
                return data
            except ValueError:
                return []
        print(f"⚠️ ERROR API ({response.status_code}): {response.url}")
        print(f"⚠️ RESPUESTA: {response.text}")
        return []

    @staticmethod
    def get(url, token=None, params=None):
        try:
            # print(f"DEBUG GET: {url}")  # Descomentar si necesitas depurar
            response = requests.get(url, headers=ApiClient._get_headers(token), params=params, timeout=5)
            return ApiClient._process_response(response)
        except requests.RequestException:
            return []

    @staticmethod
    def post(url, data, token=None):
        try:
            return requests.post(url, json=data, headers=ApiClient._get_headers(token), timeout=5)
        except requests.RequestException:
            return None

    @staticmethod
    def put(url, data=None, token=None):
        try:
            return requests.put(url, json=data, headers=ApiClient._get_headers(token), timeout=5)
        except requests.RequestException:
            return None

    @staticmethod
    def delete(url, token):
        try:
            requests.delete(url, headers=ApiClient._get_headers(token), timeout=5)
            return True
        except requests.RequestException:
            return False

    # --- Métodos de Negocio ---
    
    @staticmethod
    def get_lugares(pk=None):
        endpoint = f"{settings.API_LUGARES_URL}/lugares/"
        if pk: endpoint += f"{pk}/"
        return ApiClient.get(endpoint)

    @staticmethod
    def get_eventos(pk=None):
        endpoint = f"{settings.API_EVENTOS_URL}/eventos/"
        if pk: endpoint += f"{pk}/"
        return ApiClient.get(endpoint)

    @staticmethod
    def get_comentarios(lugar_id):
        url = f"{settings.API_INTERACCIONES_URL}/comentarios/{lugar_id}/"
        return ApiClient.get(url)