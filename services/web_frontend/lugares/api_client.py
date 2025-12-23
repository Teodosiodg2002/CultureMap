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
    def get_comentarios(recurso_id, tipo='lugar'):
        # tipo puede ser 'lugar' o 'evento'
        url = f"{settings.API_INTERACCIONES_URL}/comentarios/{tipo}/{recurso_id}/"
        return ApiClient.get(url)

    # --- Métodos de Negocio: INTERACCIONES ---

    @staticmethod
    def get_mis_favoritos(token):
        """Devuelve un dict con listas de IDs: {'lugares': [], 'eventos': []}"""
        url = f"{settings.API_INTERACCIONES_URL}/favoritos/"
        favoritos = ApiClient.get(url, token=token)
        
        resultado = {'lugares': [], 'eventos': []}
        if isinstance(favoritos, list):
            for f in favoritos:
                if f.get('lugar_id'):
                    resultado['lugares'].append(f['lugar_id'])
                elif f.get('evento_id'):
                    resultado['eventos'].append(f['evento_id'])
        return resultado

    @staticmethod
    def toggle_favorito(recurso_id, tipo, token):
        url = f"{settings.API_INTERACCIONES_URL}/favoritos/toggle/"
        data = {}
        if tipo == 'lugar': data['lugar_id'] = recurso_id
        else: data['evento_id'] = recurso_id
        
        return ApiClient.post(url, data=data, token=token)

    @staticmethod
    def enviar_voto(recurso_id, tipo, valor, token):
        url = f"{settings.API_INTERACCIONES_URL}/votar/"
        data = {'valor': valor}
        if tipo == 'lugar': data['lugar_id'] = recurso_id
        else: data['evento_id'] = recurso_id
        
        return ApiClient.post(url, data=data, token=token)

    # --- MÉTODOS NUEVOS QUE FALTABAN ---

    @staticmethod
    def get_mis_votos(token):
        """
        Devuelve un diccionario mapeando ID -> Valor.
        Ejemplo: {'lugares': {1: 5, 3: 4}, 'eventos': {10: 5}}
        """
        url = f"{settings.API_INTERACCIONES_URL}/mis-votos/"
        votos = ApiClient.get(url, token=token)
        
        resultado = {'lugares': {}, 'eventos': {}}
        if isinstance(votos, list):
            for v in votos:
                # v es {'lugar_id': 1, 'valor': 5, ...}
                if v.get('lugar_id'):
                    resultado['lugares'][v['lugar_id']] = v['valor']
                elif v.get('evento_id'):
                    resultado['eventos'][v['evento_id']] = v['valor']
        return resultado

    @staticmethod
    def get_resumen_votos(recurso_id, tipo):
        """Devuelve {'media': 4.5, 'total': 10}"""
        url = f"{settings.API_INTERACCIONES_URL}/votos/resumen/{tipo}/{recurso_id}/"
        return ApiClient.get(url)