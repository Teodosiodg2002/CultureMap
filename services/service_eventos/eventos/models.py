from django.core.validators import MinValueValidator, MaxValueValidator
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
    nombre = models.CharField(max_length=200, db_index=True)
    descripcion = models.TextField()
    
    fecha_inicio = models.DateTimeField(db_index=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    
    direccion = models.CharField(max_length=255, blank=True)
    
    # Coordenadas con validación (Consistencia con Lugares)
    lat = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        null=True, blank=True
    )
    lng = models.FloatField(
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        null=True, blank=True
    )

    categoria = models.CharField(
        max_length=20, 
        choices=CategoriaEvento.choices, 
        default=CategoriaEvento.OTROS,
        db_index=True
    )
    
    estado = models.CharField(
        max_length=20, 
        choices=EstadoEvento.choices, 
        default=EstadoEvento.PENDIENTE,
        db_index=True
    )

    creado_por_id = models.IntegerField(db_index=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Evento")
        verbose_name_plural = _("Eventos")
        ordering = ["fecha_inicio"]

    def __str__(self):
        return f"{self.nombre} ({self.fecha_inicio})"