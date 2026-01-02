"""
Django settings for CultureMapBackend project (Web Frontend).
Optimized for Railway Deployment (Microservices Architecture).
"""

import os
from pathlib import Path
import dj_database_url

# ------------------------------------------------------------------------------
# 1. CORE SETTINGS & PATHS
# ------------------------------------------------------------------------------

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Logs Directory setup
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-frontend-key')

# SECURITY WARNING: don't run with debug turned on in production!
# En Railway definiremos DEBUG=0. En local, por defecto es True.
DEBUG = os.environ.get('DEBUG', '1') == '1'

ALLOWED_HOSTS = ['*']


# ------------------------------------------------------------------------------
# 2. INSTALLED APPS
# ------------------------------------------------------------------------------

INSTALLED_APPS = [
    # Django Core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Local Apps (Frontend Logic)
    'lugares',
]


# ------------------------------------------------------------------------------
# 3. MIDDLEWARE
# ------------------------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Static files serving
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CultureMapBackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'CultureMapBackend.wsgi.application'


# ------------------------------------------------------------------------------
# 4. DATABASE (Hybrid: SQLite Local / PostgreSQL Production)
# ------------------------------------------------------------------------------

# dj_database_url.config lee automáticamente la variable 'DATABASE_URL' de Railway.
# Si no la encuentra (entorno local), usa el parámetro 'default' (SQLite).
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}


# ------------------------------------------------------------------------------
# 5. PASSWORD VALIDATION & I18N
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ------------------------------------------------------------------------------
# 6. STATIC FILES (WhiteNoise configuration)
# ------------------------------------------------------------------------------

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ------------------------------------------------------------------------------
# 7. AUTH REDIRECTS
# ------------------------------------------------------------------------------

LOGOUT_REDIRECT_URL = 'index_lugares'
LOGIN_REDIRECT_URL = 'index_lugares'


# ------------------------------------------------------------------------------
# 8. MICROSERVICES CONFIGURATION (Service Discovery)
# ------------------------------------------------------------------------------

# En local: Usamos los nombres de los servicios de Docker Compose.
# En Railway: Usaremos las variables de entorno para apuntar a los dominios .up.railway.app
API_USUARIOS_URL = os.environ.get('API_USUARIOS_URL', 'http://service-usuarios:8000/api')
API_LUGARES_URL = os.environ.get('API_LUGARES_URL', 'http://service-lugares:8000/api/catalogo')
API_INTERACCIONES_URL = os.environ.get('API_INTERACCIONES_URL', 'http://service-interacciones:8000/api/interacciones')
API_EVENTOS_URL = os.environ.get('API_EVENTOS_URL', 'http://service-eventos:8000/api')


# ------------------------------------------------------------------------------
# 9. LOGGING (JSON & Console)
# ------------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': { 
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s %(filename)s %(lineno)d',
        },
        'simple': { 
            'format': '[%(asctime)s] %(levelname)s | %(name)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console_simple': { 
            'level': 'INFO', 
            'class': 'logging.StreamHandler', 
            'formatter': 'simple',
        },
        'file_json': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'api.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 2, 
            'formatter': 'json',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console_simple', 'file_json'],
            'level': 'INFO',
            'propagate': False,
        },
        '': {
            'handlers': ['console_simple', 'file_json'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

# --- SEGURIDAD HTTPS Y CSRF ---

print("⚠️⚠️⚠️ DEBUG: CARGANDO CONFIGURACIÓN CSRF ACTUALIZADA ⚠️⚠️⚠️")
print(f"DEBUG: CSRF_TRUSTED_ORIGINS: https://culturemap-app.up.railway.app")

# 1. Confianza en el origen (Sin barra al final, con https)
CSRF_TRUSTED_ORIGINS = [
    'https://culturemap-app.up.railway.app',
    'https://*.up.railway.app'  # Comodín por si acaso
]

# 2. Configuración de Proxy (Vital para Railway)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# 3. Cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True