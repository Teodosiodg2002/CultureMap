from locust import HttpUser, task, between

class UsuarioCultureMap(HttpUser):
    # Simula que el usuario espera entre 1 y 5 segundos entre clics
    wait_time = between(1, 5)

    @task(3)
    def ver_inicio(self):
        """Carga la página principal (Index de lugares)"""
        # Ruta: path("", views.index_lugares...)
        self.client.get("/")

    @task(2)
    def ver_lista_lugares(self):
        """Carga el listado de lugares"""
        self.client.get("/lugares/")

    @task(2)
    def ver_detalle_lugar(self):
        """Entra al detalle de un lugar"""
        # Ruta: path("lugar/<int:pk>/", ...)
        self.client.get("/lugares/lugar/5/")

    @task(1)
    def ver_detalle_evento(self):
        """Entra al detalle de un evento"""
        # Ruta: path("evento/<int:pk>/", ...)
        self.client.get("/lugares/evento/4/")

    @task(1)
    def ver_ranking(self):
        """Consulta el ranking de usuarios"""
        # Ruta: path("ranking/", ...)
        self.client.get("/lugares/ranking/")
        
    @task(1)
    def ver_perfil_publico(self):
        """Visita un perfil de usuario"""
        # Ruta: path("perfil/<int:pk>/", ...)
        self.client.get("/lugares/perfil/6/")

    def on_start(self):
        """Se ejecuta al iniciar (opcional)"""
        pass