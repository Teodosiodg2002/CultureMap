from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin', _('Administrador')
        ORGANIZADOR = 'organizador', _('Organizador')
        USUARIO = 'usuario', _('Usuario Registrado')

    rol = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USUARIO
    )

    # --- GAMIFICACIÓN ---
    biografia = models.TextField(max_length=500, blank=True, null=True, help_text="Pequeña descripción pública del usuario.")
    puntos = models.IntegerField(default=0, help_text="Puntos de contribución acumulados.")

    @property
    def nivel(self):
        """Calcula el nivel en base a los puntos acumulados."""
        if self.puntos < 100: return "Novato 🐣"
        if self.puntos < 500: return "Explorador 🧭"
        if self.puntos < 1000: return "Guía Local 🗺️"
        if self.puntos < 2000: return "Experto 🏆"
        return "Leyenda 👑"

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")