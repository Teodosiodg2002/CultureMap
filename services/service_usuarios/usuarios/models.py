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

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")