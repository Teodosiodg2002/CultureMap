from django.conf import settings
from django.shortcuts import render, redirect
from django.http import Http404
import requests
from .api_client import ApiClient

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
    # 1. Obtener Lugar
    lugar = ApiClient.get_lugares(pk)
    if not lugar:
        raise Http404("Lugar no encontrado")

    # 2. Gestionar Comentario (POST)
    if request.method == 'POST':
        texto = request.POST.get('comentario')
        token = request.session.get('access_token')
        if not token: return redirect('login')
        
        if texto:
            url = f"{settings.API_INTERACCIONES_URL}/comentarios/{pk}/"
            ApiClient.post(url, {'texto': texto}, token)
        return redirect('detalle_lugar', pk=pk)

    # 3. Renderizar (GET)
    return render(request, 'lugares/detalle_lugar.html', {
        'lugar': lugar,
        'comentarios': ApiClient.get_comentarios(pk)
    })

# --- GESTIÓN DE USUARIOS (LOGIN/REGISTER) ---

def login_view(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        response = requests.post(
            f"{settings.API_USUARIOS_URL}/token/",
            json={'username': username, 'password': password}, timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            request.session['access_token'] = data.get('access')
            request.session['refresh_token'] = data.get('refresh')
            request.session['username'] = data.get('username')
            request.session['rol'] = data.get('rol')
            return redirect('index_lugares')
        else:
            return render(request, 'registration/login.html', {'error': 'Credenciales inválidas'})
            
    except requests.RequestException:
        return render(request, 'registration/login.html', {'error': 'Servicio no disponible'})

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
    return _crear_recurso(request, 'lugar', f"{settings.API_LUGARES_URL}/lugares/", 'lugares/crear_lugar.html')

def crear_evento(request):
    return _crear_recurso(request, 'evento', f"{settings.API_EVENTOS_URL}/eventos/", 'lugares/crear_evento.html')

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