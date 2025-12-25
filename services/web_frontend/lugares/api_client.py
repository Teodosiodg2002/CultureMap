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
        return []

    # --- MÉTODOS HTTP GENÉRICOS ---

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
            response = requests.post(url, json=data, headers=ApiClient._get_headers(token), timeout=5)
            # CORRECCIÓN LOGIN: Devolvemos el JSON si es 200/201
            if response.status_code in [200, 201]:
                return response.json()
            return None
        except requests.RequestException:
            return None

    @staticmethod
    def put(url, data=None, token=None):
        try:
            response = requests.put(url, json=data, headers=ApiClient._get_headers(token), timeout=5)
            if response.status_code in [200, 201]:
                return response.json()
            return None
        except requests.RequestException:
            return None
    
    @staticmethod
    def patch(url, data=None, token=None):
        try:
            response = requests.patch(url, json=data, headers=ApiClient._get_headers(token), timeout=5)
            if response.status_code in [200, 201]:
                return response.json()
            return None
        except requests.RequestException:
            return None

    @staticmethod
    def delete(url, token):
        try:
            requests.delete(url, headers=ApiClient._get_headers(token), timeout=5)
            return True
        except requests.RequestException:
            return False

    # --- LUGARES Y EVENTOS ---
    
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

    # --- INTERACCIONES (Votos, Favoritos, Comentarios) ---

    @staticmethod
    def get_comentarios(recurso_id, tipo='lugar'):
        url = f"{settings.API_INTERACCIONES_URL}/comentarios/{tipo}/{recurso_id}/"
        return ApiClient.get(url)

    @staticmethod
    def get_mis_favoritos(token):
        url = f"{settings.API_INTERACCIONES_URL}/favoritos/"
        favoritos = ApiClient.get(url, token=token)
        resultado = {'lugares': [], 'eventos': []}
        if isinstance(favoritos, list):
            for f in favoritos:
                if f.get('lugar_id'): resultado['lugares'].append(f['lugar_id'])
                elif f.get('evento_id'): resultado['eventos'].append(f['evento_id'])
        return resultado

    @staticmethod
    def toggle_favorito(recurso_id, tipo, token):
        url = f"{settings.API_INTERACCIONES_URL}/favoritos/toggle/"
        data = {'lugar_id': recurso_id} if tipo == 'lugar' else {'evento_id': recurso_id}
        return ApiClient.post(url, data=data, token=token)

    @staticmethod
    def enviar_voto(recurso_id, tipo, valor, token):
        url = f"{settings.API_INTERACCIONES_URL}/votar/"
        data = {'valor': valor, 'lugar_id' if tipo == 'lugar' else 'evento_id': recurso_id}
        return ApiClient.post(url, data=data, token=token)

    @staticmethod
    def get_mis_votos(token):
        url = f"{settings.API_INTERACCIONES_URL}/mis-votos/"
        votos = ApiClient.get(url, token=token)
        resultado = {'lugares': {}, 'eventos': {}}
        if isinstance(votos, list):
            for v in votos:
                if v.get('lugar_id'): resultado['lugares'][v['lugar_id']] = v['valor']
                elif v.get('evento_id'): resultado['eventos'][v['evento_id']] = v['valor']
        return resultado

    @staticmethod
    def get_resumen_votos(recurso_id, tipo):
        url = f"{settings.API_INTERACCIONES_URL}/votos/resumen/{tipo}/{recurso_id}/"
        return ApiClient.get(url)

    # --- USUARIOS Y GAMIFICACIÓN ---

    @staticmethod
    def get_me(token):
        """Obtiene datos del usuario logueado (ID, Rol, Puntos...)"""
        # IMPORTANTE: Asegúrate de que API_USUARIOS_URL en settings no tenga slash final extra si aquí ponemos /me/
        # Normalmente API_USUARIOS_URL es http://service-usuarios:8000/api
        url = f"{settings.API_USUARIOS_URL}/me/"
        return ApiClient.get(url, token=token)

    @staticmethod
    def get_perfil_publico(user_id):
        url = f"{settings.API_USUARIOS_URL}/{user_id}/perfil/"

        # Depende de tu urls.py del backend. Si usaste router, es 'users/'.
        return ApiClient.get(url)

    @staticmethod
    def get_ranking():
        url = f"{settings.API_USUARIOS_URL}/ranking/"
        return ApiClient.get(url)

    @staticmethod
    def sumar_puntos(user_id, cantidad, token):
        url = f"{settings.API_USUARIOS_URL}/{user_id}/puntos/"
        # Usamos PATCH para actualizar parcialmente
        return ApiClient.patch(url, data={'puntos': cantidad}, token=token)