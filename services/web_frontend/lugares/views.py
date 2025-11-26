import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import Http404

# --- VISTA: LISTA DE LUGARES ---
# services/web_frontend/lugares/views.py
def index_lugares(request):
    """
    Vista principal UNIFICADA:
    Obtiene tanto Lugares como Eventos de sus microservicios para mostrarlos juntos.
    """
    lugares = []
    eventos = []
    error = None

    # 1. Obtener Lugares (API service_lugares)
    try:
        res_lugares = requests.get(f"{settings.API_LUGARES_URL}/lugares/")
        if res_lugares.status_code == 200:
            lugares = res_lugares.json()
        else:
            error = f"Error Lugares: {res_lugares.status_code}"
    except requests.exceptions.RequestException:
        error = "Fallo al conectar con Lugares."

    # 2. Obtener Eventos (API service_eventos)
    try:
        res_eventos = requests.get(f"{settings.API_EVENTOS_URL}/eventos/")
        if res_eventos.status_code == 200:
            eventos = res_eventos.json()
        else:
            # Concatenamos errores si ya había uno
            msg = f"Error Eventos: {res_eventos.status_code}"
            error = f"{error} | {msg}" if error else msg
    except requests.exceptions.RequestException:
        msg = "Fallo al conectar con Eventos."
        error = f"{error} | {msg}" if error else msg

    # 3. Enviamos TODO a la plantilla 'index_lugares.html'
    context = {
        'lugares': lugares,
        'eventos': eventos,
        'error': error
    }
    return render(request, 'lugares/index_lugares.html', context)



# --- VISTA: DETALLE DE LUGAR ---
def detalle_lugar(request, pk):
    lugar = None
    error = None
    
    try:
        response = requests.get(f"{settings.API_LUGARES_URL}/lugares/{pk}/")
        
        if response.status_code == 200:
            lugar = response.json()
        elif response.status_code == 404:
            raise Http404("Lugar no encontrado")
        else:
            error = f"Error del servidor: {response.status_code}"
            
    except requests.exceptions.RequestException:
        error = "No se pudo conectar con el servicio de lugares."

    return render(request, 'lugares/detalle_lugar.html', {'lugar': lugar, 'error': error})


# --- VISTA: CREAR LUGAR ---
def crear_lugar(request):
    if request.method == 'GET':
        return render(request, 'lugares/crear_lugar.html')
    
    if request.method == 'POST':
        # Recuperamos el token de la sesión
        token = request.session.get('access_token')
        if not token:
            return redirect('login')
            
        headers = {'Authorization': f'Bearer {token}'}
        
        data = {
            'nombre': request.POST.get('nombre'),
            'descripcion': request.POST.get('descripcion'),
            'lat': request.POST.get('lat'),
            'lng': request.POST.get('lng'),
            'categoria': request.POST.get('categoria'),
        }
        
        try:
            response = requests.post(f"{settings.API_LUGARES_URL}/lugares/", json=data, headers=headers)
            
            if response.status_code == 201:
                return redirect('index_lugares')
            else:
                return render(request, 'lugares/crear_lugar.html', {'error': f"Error API: {response.status_code} - {response.text}"})
                
        except requests.exceptions.RequestException:
            return render(request, 'lugares/crear_lugar.html', {'error': "Error de conexión"})


# --- VISTA: REGISTRO DE USUARIO ---
def register(request):
    if request.method == 'GET':
        return render(request, 'registration/register.html')
    
    if request.method == 'POST':
        data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'password2': request.POST.get('password2'),
            # 'rol': request.POST.get('rol') 
        }
        
        try:
            response = requests.post(f"{settings.API_USUARIOS_URL}/register/", json=data)
            
            if response.status_code == 201:
                return redirect('login')
            else:
                error_msg = f"Error: {response.text}"
                return render(request, 'registration/register.html', {'error': error_msg})
                
        except requests.exceptions.RequestException:
            return render(request, 'registration/register.html', {'error': "Error de conexión con el servicio de usuarios"})


# --- VISTA: LOGIN ---
def login_view(request):
    print("=" * 60, flush=True)
    print("[VISTA] login_view iniciada", flush=True)
    print(f"[VISTA] Método: {request.method}", flush=True)
    print("=" * 60, flush=True)
    
    if request.method == 'POST':
        print("[VISTA] Procesando POST", flush=True)
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"[VISTA] Username recibido: {username}", flush=True)
        
        try:
            print("[VISTA] ANTES de llamar a service-usuarios", flush=True)
            
            response = requests.post(
                f"{settings.API_USUARIOS_URL}/token/",  # Usar settings
                json={'username': username, 'password': password},
                timeout=10
            )
            
            print(f"[VISTA] DESPUÉS de llamar a service-usuarios", flush=True)
            print(f"[VISTA] Status code: {response.status_code}", flush=True)
            print(f"[VISTA] Response: {response.text[:200]}", flush=True)
            
            if response.status_code == 200:
                print("[VISTA] Login exitoso, guardando sesión", flush=True)
                
                # ✅ GUARDAR TOKENS EN LA SESIÓN
                data = response.json()
                request.session['access_token'] = data.get('access')
                request.session['refresh_token'] = data.get('refresh')
                request.session['username'] = username
                
                print(f"[VISTA] Token guardado: {data.get('access')[:20]}...", flush=True)
                print("[VISTA] Redirigiendo a index_lugares", flush=True)
                
                # ✅ REDIRIGIR A UNA URL QUE SÍ EXISTE
                return redirect('index_lugares')
            else:
                print(f"[VISTA] Login fallido: {response.status_code}", flush=True)
                return render(request, 'registration/login.html', {  # ⚠️ Ruta corregida
                    'error': 'Credenciales inválidas'
                })
                
        except requests.Timeout:
            print("[VISTA] ⚠️ TIMEOUT al llamar a service-usuarios", flush=True)
            return render(request, 'registration/login.html', {
                'error': 'Servicio no disponible'
            })
            
        except requests.ConnectionError as e:
            print(f"[VISTA] ⚠️ ERROR DE CONEXIÓN: {e}", flush=True)
            return render(request, 'registration/login.html', {
                'error': 'No se pudo conectar al servicio'
            })
            
        except Exception as e:
            print(f"[VISTA] ⚠️ ERROR INESPERADO: {type(e).__name__}: {e}", flush=True)
            return render(request, 'registration/login.html', {
                'error': 'Error interno'
            })
    
    # GET request
    print("[VISTA] Mostrando formulario de login", flush=True)
    return render(request, 'registration/login.html') 

# --- VISTA: LISTA DE EVENTOS ---
def index_eventos(request):
    """Obtiene la lista de eventos desde el microservicio service_eventos"""
    eventos = []
    error = None

    try:
        response = requests.get(f"{settings.API_EVENTOS_URL}/eventos/")
        if response.status_code == 200:
            eventos = response.json()
        else:
            error = f"Error API Eventos: {response.status_code}"
    except requests.exceptions.RequestException:
        error = "No se pudo conectar con el servicio de eventos."

    return render(request, 'lugares/index_eventos.html', {'eventos': eventos, 'error': error})
