import requests
import json

# --- CONFIGURACIÓN DE PUERTOS (Docker) ---
# Asegúrate de que coinciden con tu compose.yaml
URL_USUARIOS = "http://localhost:8001/api"
URL_LUGARES = "http://localhost:8002/api/catalogo"
URL_INTERACCIONES = "http://localhost:8003/api/interacciones"
URL_EVENTOS = "http://localhost:8004/api"

# Colores para la consola
GREEN = '\033[92m'
RESET = '\033[0m'
RED = '\033[91m'

def print_ok(msg): print(f"{GREEN}[OK]{RESET} {msg}")
def print_err(msg): print(f"{RED}[ERROR]{RESET} {msg}")

def crear_usuario(username, email, password, rol="usuario"):
    """Registra un usuario y devuelve su token de acceso"""
    
    # --- DATOS DE REGISTRO ---
    # Usamos 'password2' porque es lo que espera tu UserRegistrationSerializer
    payload = {
        "username": username,
        "email": email,
        "password": password,
        "password2": password, 
        "rol": rol
    }
    
    print(f"Registrando a {username}...")
    
    # 1. Intentar Registrar
    try:
        res_reg = requests.post(f"{URL_USUARIOS}/register/", json=payload)
        
        if res_reg.status_code == 201:
            print_ok(f"Usuario registrado: {username} ({rol})")
        elif res_reg.status_code == 400 and "already exists" in res_reg.text:
            print(f"Usuario {username} ya existe, intentando login...")
        else:
            print_err(f"Fallo al registrar {username}: {res_reg.text}")
    except Exception as e:
        print_err(f"No se pudo conectar a usuarios: {e}")
        return None

    # 2. Login (para obtener el token)
    login_payload = {"username": username, "password": password}
    response = requests.post(f"{URL_USUARIOS}/token/", json=login_payload)
    
    if response.status_code == 200:
        print_ok(f"Token obtenido para {username}")
        return response.json()['access']
    else:
        print_err(f"No se pudo autenticar a {username}: {response.text}")
        return None

def crear_lugar(token, nombre, descripcion, lat, lng, categoria):
    """Crea un lugar usando el token de autenticación"""
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "nombre": nombre,
        "descripcion": descripcion,
        "lat": lat,
        "lng": lng,
        "categoria": categoria
    }
    res = requests.post(f"{URL_LUGARES}/lugares/", json=payload, headers=headers)
    if res.status_code == 201:
        data = res.json()
        print_ok(f"Lugar propuesto: {nombre} (ID: {data['id']})")
        return data['id']
    else:
        print_err(f"Error creando lugar {nombre}: {res.text}")
        return None

def aprobar_lugar(token_admin, lugar_id):
    """Aprueba un lugar usando el endpoint de moderación (requiere ser Admin/Organizador)"""
    headers = {"Authorization": f"Bearer {token_admin}"}
    # La URL depende de cómo definiste el router y la acción @action en views.py
    # Normalmente es .../lugares/{id}/aprobar/
    res = requests.put(f"{URL_LUGARES}/lugares/{lugar_id}/aprobar/", headers=headers)
    
    if res.status_code == 200:
        print_ok(f"Lugar {lugar_id} APROBADO y visible.")
    else:
        print_err(f"Fallo al aprobar lugar {lugar_id}: {res.status_code} - {res.text}")

def crear_evento(token, nombre, descripcion, lat, lng, fecha_inicio):
    """Crea un evento"""
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "nombre": nombre,
        "descripcion": descripcion,
        "lat": lat,
        "lng": lng,
        "fecha_inicio": fecha_inicio,
        "categoria": "concierto" 
    }
    # Ajusta la URL si tu router de eventos tiene otro prefijo (ej. /eventos/)
    res = requests.post(f"{URL_EVENTOS}/eventos/", json=payload, headers=headers)
    if res.status_code == 201:
        print_ok(f"Evento creado: {nombre}")
    else:
        print_err(f"Error creando evento {nombre}: {res.text}")

# ============================================================================
# EJECUCIÓN DEL SCRIPT
# ============================================================================

print("--- 🚀 INICIANDO POBLACIÓN DE DATOS CULTUREMAP ---")

# 1. CREAR USUARIOS
# Creamos un Admin (para aprobar cosas)
token_admin = crear_usuario("admin_granada", "admin@granada.es", "cultura2025", "admin")

# Creamos un Organizador (para proponer cosas)
token_org = crear_usuario("organizador_jazz", "jazz@granada.es", "jazz2025", "organizador")

# Creamos un Viajero (para visitar)
token_viajero = crear_usuario("mochilero_1", "viajero@gmail.com", "viaje123", "usuario")

if not token_org or not token_admin:
    print_err("Fallo crítico: No se obtuvieron los tokens necesarios. Abortando.")
    exit()

# 2. CREAR LUGARES (El organizador propone)
print("\n--- Creando Lugares ---")
id_mirador = crear_lugar(token_org, "Mirador de San Nicolás", 
            "El mirador más emblemático de Granada, con las mejores vistas a la Alhambra.", 
            37.1811, -3.5928, "mirador")

id_bar = crear_lugar(token_org, "Bodegas Castañeda", 
            "Un clásico para tapear en Granada. Vinos de la tierra y ambiente auténtico.", 
            37.1772, -3.5983, "bar")

id_tienda = crear_lugar(token_org, "Librería Babel", 
            "Librería con encanto especializada en arte y música.", 
            37.1750, -3.6000, "tienda")

# 3. APROBAR LUGARES (El admin aprueba)
# IMPORTANTE: Si no se aprueban, la API pública (y el frontend) no los mostrará.
print("\n--- Aprobando Lugares (Moderación) ---")
if id_mirador: aprobar_lugar(token_admin, id_mirador)
if id_bar: aprobar_lugar(token_admin, id_bar)
if id_tienda: aprobar_lugar(token_admin, id_tienda)

# 4. CREAR EVENTOS
print("\n--- Creando Eventos ---")
crear_evento(token_org, "Festival Internacional de Jazz", 
             "Conciertos al aire libre.", 
             37.1773, -3.5986, "2025-11-15T20:00:00Z")

crear_evento(token_org, "Noche en Blanco", 
             "Museos abiertos toda la noche.", 
             37.1760, -3.5990, "2025-10-20T18:00:00Z")

print("\n--- ✅ POBLACIÓN COMPLETADA ---")