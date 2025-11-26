import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CultureMapBackend.settings')

# Middleware de debugging
class DebugMiddleware:
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        print("=" * 60, flush=True)
        print(f"[WSGI DEBUG] Petición recibida!", flush=True)
        print(f"[WSGI DEBUG] Método: {environ.get('REQUEST_METHOD')}", flush=True)
        print(f"[WSGI DEBUG] Path: {environ.get('PATH_INFO')}", flush=True)
        print(f"[WSGI DEBUG] Content-Length: {environ.get('CONTENT_LENGTH', 'N/A')}", flush=True)
        print("=" * 60, flush=True)
        return self.app(environ, start_response)

application = get_wsgi_application()
application = DebugMiddleware(application)