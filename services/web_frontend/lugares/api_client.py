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
        
        # Debugging silencioso (puedes descomentar si hay errores)
        # print(f"⚠️ ERROR API ({response.status_code}): {response.url}")
        return []

    @staticmethod
    def get(url, token=None, params=None):
        try:
            response = requests.get(url, headers=ApiClient._get_headers(token), params=params, timeout=5)
            return ApiClient._process_response(response)
        except requests.RequestException:
            return []

    @staticmethod
    def post(url, data=None, token=None):
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

    # --- Métodos de Negocio: LECTURA ---
    
    @staticmethod
    def get_lugares(pk=None, token=None):
        endpoint = f"{settings.API_LUGARES_URL}/lugares/"
        if pk: endpoint += f"{pk}/"
        return ApiClient.get(endpoint, token=token)

    @staticmethod
    def get_eventos(pk=None, token=None):
        endpoint = f"{settings.API_EVENTOS_URL}/eventos/"
        if pk: endpoint += f"{pk}/"
        return ApiClient.get(endpoint, token=token)

    @staticmethod
    def get_comentarios(lugar_id):
        # Los comentarios son públicos, no requieren token obligatoriamente
        url = f"{settings.API_INTERACCIONES_URL}/comentarios/{lugar_id}/"
        return ApiClient.get(url)

    # --- Métodos de Negocio: INTERACCIONES (NUEVO) ---

    @staticmethod
    def get_mis_favoritos(token):
        """Obtiene la lista de IDs de lugares favoritos del usuario."""
        url = f"{settings.API_INTERACCIONES_URL}/favoritos/"
        favoritos = ApiClient.get(url, token=token)
        # Devolvemos solo una lista de IDs para facilitar la comprobación en el template: [1, 5, 8]
        if isinstance(favoritos, list):
            return [f['lugar_id'] for f in favoritos if 'lugar_id' in f]
        return []

    @staticmethod
    def toggle_favorito(lugar_id, token):
        url = f"{settings.API_INTERACCIONES_URL}/favoritos/toggle/"
        return ApiClient.post(url, data={'lugar_id': lugar_id}, token=token)

    @staticmethod
    def enviar_voto(lugar_id, valor, token):
        url = f"{settings.API_INTERACCIONES_URL}/votar/"
        return ApiClient.post(url, data={'lugar_id': lugar_id, 'valor': valor}, token=token)