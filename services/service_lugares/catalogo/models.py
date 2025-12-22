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
    nombre = models.CharField(max_length=200, db_index=True)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=255, blank=True, null=True)

    lat = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        null=True, blank=True
    )
    lng = models.FloatField(
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        null=True, blank=True
    )

    categoria = models.CharField(
        max_length=30, 
        choices=Categoria.choices, 
        default=Categoria.OTROS,
        db_index=True
    )

    estado = models.CharField(
        max_length=20, 
        choices=EstadoAprobacion.choices, 
        default=EstadoAprobacion.PENDIENTE,
        db_index=True
    )
    motivo_rechazo = models.TextField(blank=True, null=True)
    publicado = models.BooleanField(default=True, db_index=True)  

    creado_por_id = models.IntegerField(db_index=True)
    creado_en = models.DateTimeField(auto_now_add=True, db_index=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Lugar")
        verbose_name_plural = _("Lugares")
        ordering = ["-creado_en"]
        indexes = [
            models.Index(fields=["lat", "lng"], name="idx_lugar_coords"),
            models.Index(fields=["categoria", "estado", "publicado"], name="idx_lugar_filtros"),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"

    @property
    def esta_aprobado(self):
        return self.estado == EstadoAprobacion.APROBADO