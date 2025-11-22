from django.db import models
from django.utils.translation import gettext_lazy as _

class CategoriaEvento(models.TextChoices):
    CONCIERTO = "concierto", _("Concierto")
    EXPOSICION = "exposicion", _("Exposición")
    TEATRO = "teatro", _("Teatro")
    CHARLA = "charla", _("Charla/Conferencia")
    FIESTA = "fiesta", _("Fiesta popular")
    OTROS = "otros", _("Otros")

class EstadoEvento(models.TextChoices):
    PENDIENTE = "pendiente", _("Pendiente de revisión")
    PUBLICADO = "publicado", _("Publicado")
    CANCELADO = "cancelado", _("Cancelado")

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)
    
    lat = models.FloatField()
    lng = models.FloatField()
    direccion = models.CharField(max_length=255, blank=True)

    categoria = models.CharField(
        max_length=20, 
        choices=CategoriaEvento.choices, 
        default=CategoriaEvento.OTROS
    )
    
    estado = models.CharField(
        max_length=20, 
        choices=EstadoEvento.choices, 
        default=EstadoEvento.PENDIENTE
    )

    creado_por_id = models.IntegerField()
    
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre