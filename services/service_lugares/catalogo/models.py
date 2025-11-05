# services/service_lugares/catalogo/models.py

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Categoria(models.TextChoices):
    MIRADOR = "mirador", _("Mirador")
    BAR = "bar", _("Bar con encanto")
    GALERIA = "galeria", _("Galería")
    TIENDA = "tienda", _("Tienda local")
    ARTE_URBANO = "arte_urbano", _("Arte urbano")
    PLAZA = "plaza", _("Plaza")
    OTROS = "otros", _("Otros")

class EstadoAprobacion(models.TextChoices):
    PENDIENTE = "pendiente", _("Pendiente de revisión")
    APROBADO = "aprobado", _("Aprobado")
    RECHAZADO = "rechazado", _("Rechazado")

class Lugar(models.Model):

    nombre = models.CharField(max_length=200, verbose_name=_("Nombre del lugar"), db_index=True)
    descripcion = models.TextField(verbose_name=_("Descripción"))    
    direccion = models.CharField(max_length=255, verbose_name=_("Dirección"), blank=True, null=True)

    lat = models.FloatField(
        verbose_name=_("Latitud"),
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        null=True, blank=True
    )
    lng = models.FloatField(
        verbose_name=_("Longitud"),
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        null=True, blank=True
    )

    categoria = models.CharField(
        max_length=30, 
        choices=Categoria.choices, 
        default=Categoria.OTROS, 
        verbose_name=_("Categoría"), 
        db_index=True
    )

    estado = models.CharField(
        max_length=20, 
        choices=EstadoAprobacion.choices, 
        default=EstadoAprobacion.PENDIENTE, 
        verbose_name=_("Estado de aprobación"), 
        db_index=True
    )
    motivo_rechazo = models.TextField(verbose_name=_("Motivo de rechazo"), blank=True, null=True)
    publicado = models.BooleanField(default=True, verbose_name=_("Publicado"), db_index=True)  

    creado_por_id = models.IntegerField(verbose_name=_("ID del creador"), db_index=True)

    creado_en = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creación"), db_index=True)
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name=_("Última actualización"))

    class Meta:
        verbose_name = _("Lugar")
        verbose_name_plural = _("Lugares")
        ordering = ["-creado_en"]
        indexes = [
            models.Index(fields=["lat", "lng"], name="idx_lugar_coords"),
            models.Index(fields=["categoria", "estado", "publicado"], name="idx_lugar_filtros"),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"

    @property
    def esta_aprobado(self):
        return self.estado == EstadoAprobacion.APROBADO

    @property
    def es_visible(self):
        return self.esta_aprobado and self.publicado
