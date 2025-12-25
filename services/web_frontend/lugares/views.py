from django.conf import settings
from django.shortcuts import render, redirect
from django.http import Http404
import requests
from .api_client import ApiClient

PUNTOS_CREAR_LUGAR = 50
PUNTOS_CREAR_EVENTO = 30
PUNTOS_COMENTAR = 5

# --- VISTAS PÚBLICAS ---

def index_lugares(request):
    return render(request, 'lugares/index_lugares.html', {
        'lugares': ApiClient.get_lugares(),
        'eventos': ApiClient.get_eventos()
    })

def index_eventos(request):
    return render(request, 'lugares/index_eventos.html', {
        'eventos': ApiClient.get_eventos()
    })

def detalle_lugar(request, pk):
    lugar = ApiClient.get_lugares(pk)
    if not lugar:
        raise Http404("Lugar no encontrado")

    # 1. GESTIÓN DE COMENTARIOS (POST)
    if request.method == 'POST':
        texto = request.POST.get('comentario')
        token = request.session.get('access_token')
        if not token: return redirect('login')
        
        if texto:
            ApiClient.post(f"{settings.API_INTERACCIONES_URL}/comentarios/lugar/{pk}/", {'texto': texto}, token)
        return redirect('detalle_lugar', pk=pk)

    # 2. DATOS DE INTERACCIÓN (Lectura)
    es_favorito = False
    mi_voto = 0
    token = request.session.get('access_token')

    if token:
        # A. Verificar Favorito
        favs = ApiClient.get_mis_favoritos(token)
        if int(pk) in favs.get('lugares', []):
            es_favorito = True
        
        # B. Verificar Mi Voto (Para pintar mis estrellas)
        mis_votos = ApiClient.get_mis_votos(token)
        mi_voto = mis_votos['lugares'].get(int(pk), 0)

    # 3. PUNTUACIÓN GLOBAL (Media de todos)
    puntuacion = ApiClient.get_resumen_votos(pk, tipo='lugar')

    return render(request, 'lugares/detalle_lugar.html', {
        'lugar': lugar,
        'comentarios': ApiClient.get_comentarios(pk, tipo='lugar'),
        'es_favorito': es_favorito,
        'mi_voto': mi_voto,      # Lo que yo voté (ej: 4)
        'puntuacion': puntuacion # La media global (ej: {'media': 4.5, 'total': 12})
    })
    
def detalle_evento(request, pk):
    evento = ApiClient.get_eventos(pk)
    if not evento:
        raise Http404("Evento no encontrado")

    # 1. GESTIÓN DE COMENTARIOS (POST)
    if request.method == 'POST':
        texto = request.POST.get('comentario')
        token = request.session.get('access_token')
        if not token: return redirect('login')
        
        if texto:
            ApiClient.post(f"{settings.API_INTERACCIONES_URL}/comentarios/evento/{pk}/", {'texto': texto}, token)
        return redirect('detalle_evento', pk=pk)

    # 2. DATOS DE INTERACCIÓN
    es_favorito = False
    mi_voto = 0
    token = request.session.get('access_token')

    if token:
        # A. Verificar Favorito
        favs = ApiClient.get_mis_favoritos(token)
        if int(pk) in favs.get('eventos', []):
            es_favorito = True
            
        # B. Verificar Mi Voto
        mis_votos = ApiClient.get_mis_votos(token)
        mi_voto = mis_votos['eventos'].get(int(pk), 0)

    # 3. PUNTUACIÓN GLOBAL
    puntuacion = ApiClient.get_resumen_votos(pk, tipo='evento')

    return render(request, 'lugares/detalle_evento.html', {
        'evento': evento,
        'comentarios': ApiClient.get_comentarios(pk, tipo='evento'),
        'es_favorito': es_favorito,
        'mi_voto': mi_voto,
        'puntuacion': puntuacion
    })
    
# --- GESTIÓN DE USUARIOS (LOGIN/REGISTER) ---

def login_view(request):
    # Si ya está logueado, fuera
    if request.session.get('access_token'):
        return redirect('index_lugares')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        print(f"DEBUG LOGIN: Intentando entrar con usuario: {username}")

        # 1. URL del Login
        url_login = f"{settings.API_USUARIOS_URL}/login/"
        print(f"DEBUG LOGIN: URL endpoint -> {url_login}")
        
        # 2. Llamada a la API
        auth_data = ApiClient.post(url_login, {
            "username": username,
            "password": password
        })
        
        print(f"DEBUG LOGIN: Respuesta del Backend -> {auth_data}")

        if auth_data and "access" in auth_data:
            print("DEBUG LOGIN: ¡Token recibido! Guardando sesión...")
            token = auth_data["access"]
            request.session['access_token'] = token
            request.session['username'] = username
            
            # 3. Obtener Datos de Usuario (ID y Rol)
            me = ApiClient.get_me(token)
            print(f"DEBUG LOGIN: Datos de perfil (me) -> {me}")
            
            if me:
                request.session['user_id'] = me.get('id')
                request.session['rol'] = me.get('rol')
            
            return redirect('index_lugares')
        else:
            print("DEBUG LOGIN: Fallo. Credenciales incorrectas o error de conexión.")
            return render(request, "lugares/login.html", {"error": "Credenciales inválidas o error de servidor"})
    
    return render(request, "lugares/login.html")


def logout_view(request):
    request.session.flush()
    return redirect('index_lugares')

def register(request):
    if request.method == 'GET':
        return render(request, 'registration/register.html')

    data = {k: request.POST.get(k) for k in ['username', 'email', 'password', 'password2']}
    
    try:
        res = requests.post(f"{settings.API_USUARIOS_URL}/register/", json=data, timeout=5)
        if res.status_code == 201:
            return redirect('login')
        return render(request, 'registration/register.html', {'error': f"Error: {res.text}"})
    except requests.RequestException:
        return render(request, 'registration/register.html', {'error': "Error de conexión"})

# --- CREACIÓN DE RECURSOS ---

def seleccionar_creacion(request):
    if not request.session.get('access_token'): return redirect('login')
    return render(request, 'lugares/seleccionar_creacion.html')

def _crear_recurso(request, tipo, url_api, template):
    """Helper genérico para crear lugares o eventos."""
    if request.method == 'GET':
        if not request.session.get('access_token'): return redirect('login')
        return render(request, template)

    token = request.session.get('access_token')
    data = request.POST.dict() # Convierte QueryDict a dict plano
    # Eliminamos el token csrf del dict si existe
    data.pop('csrfmiddlewaretoken', None)

    res = ApiClient.post(url_api, data, token)
    if res and res.status_code == 201:
        return redirect('index_lugares')
    
    error_msg = res.text if res else "Error de conexión"
    return render(request, template, {'error': f"Error: {error_msg}"})

def crear_lugar(request):
    if request.method == 'POST':
        token = request.session.get('access_token')
        user_id = request.session.get('user_id') # Recuperamos el ID

        data = {
            'nombre': request.POST.get('nombre'),
            'descripcion': request.POST.get('descripcion'),
            'lat': float(request.POST.get('lat')),
            'lng': float(request.POST.get('lng')),
            'categoria': request.POST.get('categoria'),
            'usuario_id': user_id  # Enviamos el ID real
        }

        response = ApiClient.post(f"{settings.API_LUGARES_URL}/lugares/", data, token)

        if response and response.get('id'):
            # ¡PREMIO! Sumamos puntos
            ApiClient.sumar_puntos(user_id, PUNTOS_CREAR_LUGAR, token)
            return redirect('index_lugares')
        else:
            return render(request, 'lugares/crear_lugar.html', {'error': 'Error al crear lugar'})

    return render(request, 'lugares/crear_lugar.html')

def crear_evento(request):
    if request.method == 'POST':
        token = request.session.get('access_token')
        user_id = request.session.get('user_id')

        data = {
            'nombre': request.POST.get('nombre'),
            'descripcion': request.POST.get('descripcion'),
            'fecha_inicio': request.POST.get('fecha_inicio'),
            'lat': float(request.POST.get('lat')),
            'lng': float(request.POST.get('lng')),
            'categoria': request.POST.get('categoria'),
            'usuario_id': user_id
        }

        response = ApiClient.post(f"{settings.API_EVENTOS_URL}/eventos/", data, token)

        if response and response.get('id'):
            # ¡PREMIO! Sumamos puntos
            ApiClient.sumar_puntos(user_id, PUNTOS_CREAR_EVENTO, token)
            return redirect('index_eventos')
        else:
            return render(request, 'lugares/crear_evento.html', {'error': 'Error al crear evento'})

    return render(request, 'lugares/crear_evento.html')

# --- DASHBOARD Y ADMINISTRACIÓN ---

def dashboard(request):
    rol = request.session.get('rol')
    token = request.session.get('access_token')
    
    print(f"--- DEBUG DASHBOARD ---")
    print(f"Rol: {rol}")
    
    if not token or rol not in ['admin', 'organizador']:
        return redirect('index_lugares')

    # Llamada a la API
    print("Pidiendo lugares...")
    lugares = ApiClient.get(f"{settings.API_LUGARES_URL}/lugares/", token=token)
    
    # --- LA LINTERNA (IMPRIMIR DATOS) ---
    print(f"TIPO de datos Lugares: {type(lugares)}")
    print(f"CONTENIDO de Lugares (Primeros 100 chars): {str(lugares)[:100]}")
    
    if isinstance(lugares, list) and len(lugares) > 0:
        print(f"Primer lugar: {lugares[0]}")
    elif isinstance(lugares, dict):
        print(f"⚠️ CUIDADO: Lugares es un DICCIONARIO, claves: {lugares.keys()}")
    # ------------------------------------

    eventos = ApiClient.get(f"{settings.API_EVENTOS_URL}/eventos/", token=token)
    
    usuarios = []
    if rol == 'admin':
        usuarios = ApiClient.get(f"{settings.API_USUARIOS_URL}/users/", token=token)

    return render(request, 'lugares/dashboard.html', {
        'lugares': lugares,
        'eventos': eventos,
        'usuarios': usuarios,
        'total_lugares': len(lugares) if isinstance(lugares, list) else 0,
        'total_eventos': len(eventos) if isinstance(eventos, list) else 0,
        'total_usuarios': len(usuarios) if isinstance(usuarios, list) else 0
    })

def borrar_recurso(request, tipo, pk):
    if request.method != 'POST': return redirect('dashboard')
    token = request.session.get('access_token')
    
    urls = {
        'lugar': f"{settings.API_LUGARES_URL}/lugares/{pk}/",
        'evento': f"{settings.API_EVENTOS_URL}/eventos/{pk}/",
        'usuario': f"{settings.API_USUARIOS_URL}/users/{pk}/"
    }
    
    if tipo in urls:
        ApiClient.delete(urls[tipo], token)
    
    return redirect('dashboard')

def cambiar_rol(request, pk):
    if request.method == 'POST':
        token = request.session.get('access_token')
        url = f"{settings.API_USUARIOS_URL}/users/{pk}/"
        # PATCH manual porque ApiClient no tiene patch
        requests.patch(url, json={'rol': request.POST.get('rol')}, headers={'Authorization': f'Bearer {token}'})
    return redirect('dashboard')

def gestionar_recurso(request, tipo, pk, accion):
    if request.method != 'POST': return redirect('dashboard')
    token = request.session.get('access_token')
    
    base = settings.API_LUGARES_URL if tipo == 'lugar' else settings.API_EVENTOS_URL
    endpoint = 'lugares' if tipo == 'lugar' else 'eventos'
    
    url = f"{base}/{endpoint}/{pk}/{accion}/"
    ApiClient.put(url, token=token)
    
    return redirect('dashboard')

def accion_favorito(request, tipo, pk):
    """Maneja el clic en el corazón para Lugares O Eventos"""
    if request.method == 'POST':
        token = request.session.get('access_token')
        if not token: return redirect('login')
        
        # tipo vendrá como 'lugar' o 'evento' desde la URL
        ApiClient.toggle_favorito(pk, tipo, token)
        
    # Redirección dinámica según el tipo
    if tipo == 'evento':
        return redirect('detalle_evento', pk=pk)
    return redirect('detalle_lugar', pk=pk)

def accion_votar(request, tipo, pk, valor):
    """Maneja el clic en las Estrellas (1-5)"""
    if request.method == 'POST':
        token = request.session.get('access_token')
        if not token: return redirect('login')
        
        ApiClient.enviar_voto(pk, tipo, int(valor), token)
        
    if tipo == 'evento':
        return redirect('detalle_evento', pk=pk)
    return redirect('detalle_lugar', pk=pk)

def ver_ranking(request):
    ranking = ApiClient.get_ranking()
    return render(request, 'lugares/ranking.html', {'ranking': ranking})

def ver_perfil(request, pk):
    print(f"DEBUG PERFIL: Buscando perfil ID: {pk}")
    
    perfil = ApiClient.get_perfil_publico(pk)
    print(f"DEBUG PERFIL: Respuesta recibida: {perfil}")

    if not perfil:
        print("DEBUG PERFIL: Fallo. Redirigiendo a home...")
        return redirect('index_lugares')
        
    return render(request, 'lugares/perfil_publico.html', {'perfil': perfil})