import requests
import sys

# ==========================================
# CONFIGURACIÓN DE CONEXIÓN
# ==========================================
URL_USUARIOS = "http://localhost:8001/api"
URL_LUGARES = "http://localhost:8002/api/catalogo"
URL_EVENTOS = "http://localhost:8004/api"

# Credenciales del Administrador
# Solo para la carga incial de datos
 
ADMIN_USER = "admin_general"
ADMIN_PASS = "admin1234"
ADMIN_EMAIL = "admin@culturemap.com"

# ==========================================
# DATOS A INSERTAR (Granada y alrededores)
# ==========================================

# 10 Lugares con coordenadas separadas
DATOS_LUGARES = [
    {"nombre": "La Alhambra", "cat": "monumento", "lat": 37.1760, "lng": -3.5875, "desc": "Palacio y fortaleza nazarí."},
    {"nombre": "Mirador de San Nicolás", "cat": "mirador", "lat": 37.1811, "lng": -3.5928, "desc": "Vistas panorámicas a la Alhambra."},
    {"nombre": "Catedral de Granada", "cat": "monumento", "lat": 37.1766, "lng": -3.5991, "desc": "Obra maestra del Renacimiento español."},
    {"nombre": "Parque de las Ciencias", "cat": "otros", "lat": 37.1626, "lng": -3.6056, "desc": "Museo interactivo de ciencia."},
    {"nombre": "Paseo de los Tristes", "cat": "plaza", "lat": 37.1785, "lng": -3.5890, "desc": "Paseo junto al río Darro."},
    {"nombre": "Monasterio de la Cartuja", "cat": "monumento", "lat": 37.1920, "lng": -3.5998, "desc": "Joya del barroco español."},
    {"nombre": "Plaza Nueva", "cat": "plaza", "lat": 37.1770, "lng": -3.5960, "desc": "Centro neurálgico de la ciudad."},
    {"nombre": "Sacromonte", "cat": "otros", "lat": 37.1830, "lng": -3.5800, "desc": "Barrio de cuevas y flamenco."},
    {"nombre": "Carmen de los Mártires", "cat": "mirador", "lat": 37.1730, "lng": -3.5850, "desc": "Jardines románticos y vistas."},
    {"nombre": "Palacio de Carlos V", "cat": "monumento", "lat": 37.1768, "lng": -3.5899, "desc": "Edificio renacentista dentro de la Alhambra."}
]

# 10 Eventos con coordenadas separadas (algunos coinciden con lugares, otros no)
DATOS_EVENTOS = [
    {"nombre": "Festival de Jazz", "cat": "concierto", "lat": 37.1773, "lng": -3.5986, "fecha": "2025-11-15T21:00:00Z", "desc": "Jazz en vivo."},
    {"nombre": "Feria del Libro", "cat": "exposicion", "lat": 37.1700, "lng": -3.6000, "fecha": "2025-05-20T10:00:00Z", "desc": "Casetas y firmas."},
    {"nombre": "Noche en Blanco", "cat": "fiesta", "lat": 37.1750, "lng": -3.6020, "fecha": "2025-10-20T18:00:00Z", "desc": "Cultura nocturna."},
    {"nombre": "Concierto Flamenco", "cat": "concierto", "lat": 37.1835, "lng": -3.5805, "fecha": "2025-06-15T22:00:00Z", "desc": "En cueva del Sacromonte."},
    {"nombre": "Teatro en la calle", "cat": "teatro", "lat": 37.1765, "lng": -3.5992, "fecha": "2025-07-01T19:00:00Z", "desc": "Actuaciones urbanas."},
    {"nombre": "Exposición Goya", "cat": "exposicion", "lat": 37.1768, "lng": -3.5899, "fecha": "2025-09-10T09:00:00Z", "desc": "Grabados originales."},
    {"nombre": "Mercado Medieval", "cat": "otros", "lat": 37.1785, "lng": -3.5890, "fecha": "2025-04-12T11:00:00Z", "desc": "Artesanía y comida."},
    {"nombre": "Cine de Verano", "cat": "otros", "lat": 37.1626, "lng": -3.6056, "fecha": "2025-08-05T22:00:00Z", "desc": "Películas al aire libre."},
    {"nombre": "Ruta de Tapas", "cat": "fiesta", "lat": 37.1772, "lng": -3.5983, "fecha": "2025-03-01T13:00:00Z", "desc": "Gastronomía local."},
    {"nombre": "Danza Contemporánea", "cat": "teatro", "lat": 37.1740, "lng": -3.6010, "fecha": "2025-11-30T20:00:00Z", "desc": "Festival de danza."}
]

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def obtener_token_admin():
    """Registra (si no existe) y loguea al admin para obtener el token."""
    print(f"Procesando usuario: {ADMIN_USER}...")
    
    # 1. Registro
    datos_registro = {
        "username": ADMIN_USER,
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASS,
        "password2": ADMIN_PASS,
        "rol": "admin"
    }
    try:
        requests.post(f"{URL_USUARIOS}/register/", json=datos_registro)
    except requests.exceptions.ConnectionError:
        print("ERROR CRÍTICO: No se puede conectar con service-usuarios. ¿Docker está encendido?")
        sys.exit(1)

    # 2. Login
    res = requests.post(f"{URL_USUARIOS}/token/", json={"username": ADMIN_USER, "password": ADMIN_PASS})
    
    if res.status_code == 200:
        print("Login correcto. Token obtenido.")
        return res.json()['access']
    else:
        print(f"Error en login: {res.text}")
        sys.exit(1)

def gestionar_lugar(token, datos):
    """Crea un lugar y lo aprueba."""
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Crear
    payload = {
        "nombre": datos['nombre'],
        "descripcion": datos['desc'],
        "lat": datos['lat'],
        "lng": datos['lng'],
        "categoria": datos['cat']
    }
    res = requests.post(f"{URL_LUGARES}/lugares/", json=payload, headers=headers)
    
    if res.status_code == 201:
        lugar_id = res.json()['id']
        print(f"Lugar creado: {datos['nombre']} (ID: {lugar_id})")
        
        # 2. Aprobar
        requests.put(f"{URL_LUGARES}/lugares/{lugar_id}/aprobar/", headers=headers)
    else:
        print(f"Error creando lugar {datos['nombre']}: {res.status_code}")

def gestionar_evento(token, datos):
    """Crea un evento y lo aprueba."""
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Crear
    payload = {
        "nombre": datos['nombre'],
        "descripcion": datos['desc'],
        "lat": datos['lat'],
        "lng": datos['lng'],
        "categoria": datos['cat'],
        "fecha_inicio": datos['fecha']
    }
    res = requests.post(f"{URL_EVENTOS}/eventos/", json=payload, headers=headers)
    
    if res.status_code == 201:
        evento_id = res.json()['id']
        print(f"Evento creado: {datos['nombre']} (ID: {evento_id})")
        
        # 2. Aprobar
        requests.put(f"{URL_EVENTOS}/eventos/{evento_id}/aprobar/", headers=headers)
    else:
        print(f"Error creando evento {datos['nombre']}: {res.status_code}")

# ==========================================
# EJECUCIÓN PRINCIPAL
# ==========================================

if __name__ == "__main__":
    print("--- INICIANDO CARGA DE DATOS ---")
    
    # 1. Obtener credenciales
    token = obtener_token_admin()
    
    # 2. Procesar Lugares
    print("\n--- Insertando 10 Lugares ---")
    for lugar in DATOS_LUGARES:
        gestionar_lugar(token, lugar)
        
    # 3. Procesar Eventos
    print("\n--- Insertando 10 Eventos ---")
    for evento in DATOS_EVENTOS:
        gestionar_evento(token, evento)
        
    print("\n--- FIN DEL PROCESO ---")