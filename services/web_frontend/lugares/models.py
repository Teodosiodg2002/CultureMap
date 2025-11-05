"""
Modelos de datos para CultureMap.

Este módulo define las entidades principales del sistema:
- Lugar: Sitios culturales propuestos por usuarios
- Categoria: Tipos de lugares (Enum)
- Favorito: Relación usuario-lugar favorito
- Comentario: Comentarios de usuarios en lugares
- Voto: Sistema de votación (upvote/downvote)

Autor: Teodosio Donaire González
Proyecto: CultureMap - Master en Ingeniería Informática UGR
"""

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _



# ============================================================================
# ENUMERACIONES Y CONSTANTES
# ============================================================================
class Categoria(models.TextChoices):
    """
    Categorías disponibles para clasificar lugares culturales.

    Se usa TextChoices para:
    - Validación automática en base de datos
    
    """
    MIRADOR = "mirador", _("Mirador")
    BAR = "bar", _("Bar con encanto")
    GALERIA = "galeria", _("Galería")
    TIENDA = "tienda", _("Tienda local")
    ARTE_URBANO = "arte_urbano", _("Arte urbano")
    EXPOSICION = "exposicion", _("Exposición")
    CHARLA = "charla", _("Charla")
    CONCIERTO = "concierto", _("Concierto")
    PLAZA = "plaza", _("Plaza")
    OTROS = "otros", _("Otros")


class EstadoAprobacion(models.TextChoices):
    
    PENDIENTE = "pendiente", _("Pendiente de revisión")
    APROBADO = "aprobado", _("Aprobado")
    RECHAZADO = "rechazado", _("Rechazado")


# ============================================================================
# MODELO PRINCIPAL: LUGAR
# ============================================================================

class Lugar(models.Model):
    """
    Modelo principal que representa un lugar cultural en el mapa.
    
    Incluye:
    - Información básica (nombre, descripción, ubicación)
    - Geolocalización (latitud/longitud)
    - Sistema de moderación (estado de aprobación)
    - Info (creador, fechas)
    
    Attributes:
        nombre (str): Nombre del lugar (máx. 200 caracteres)
        descripcion (str): Descripción detallada
        direccion (str): Dirección física completa
        lat (float): Latitud (rango: -90 a 90)
        lng (float): Longitud (rango: -180 a 180)
        categoria (str): Tipo de lugar (choices de Categoria)
        creado_por (User): Usuario que propuso el lugar
        estado (str): Estado de moderación (pendiente/aprobado/rechazado)
        motivo_rechazo (str): Razón del rechazo (si aplica)
        publicado (bool): Visibilidad pública
        creado_en (datetime): Fecha de creación
        actualizado_en (datetime): Última modificación
    """
    
    # ──────────────────────────────────────────────────────────────────────
    # CAMPOS DE INFORMACIÓN BÁSICA
    # ──────────────────────────────────────────────────────────────────────
    
    nombre = models.CharField(max_length=200, verbose_name=_("Nombre del lugar"), db_index=True)
    descripcion = models.TextField(verbose_name=_("Descripción"))    
    direccion = models.CharField(max_length=255, verbose_name=_("Dirección"), blank=True, null=True)
    
    # ──────────────────────────────────────────────────────────────────────
    # CAMPOS DE GEOLOCALIZACIÓN
    # ──────────────────────────────────────────────────────────────────────
    
    lat = models.FloatField(
        verbose_name=_("Latitud"),
        validators=[
            MinValueValidator(-90.0, message=_("La latitud debe ser >= -90")),
            MaxValueValidator(90.0, message=_("La latitud debe ser <= 90"))
        ],
        null=True,
        blank=True
    )
    
    lng = models.FloatField(
        verbose_name=_("Longitud"),
        validators=[
            MinValueValidator(-180.0, message=_("La longitud debe ser >= -180")),
            MaxValueValidator(180.0, message=_("La longitud debe ser <= 180"))
        ],
        null=True,
        blank=True
    )
    
    # ──────────────────────────────────────────────────────────────────────
    # CAMPOS DE CLASIFICACIÓN
    # ──────────────────────────────────────────────────────────────────────
    
    categoria = models.CharField(max_length=30, choices=Categoria.choices, default=Categoria.OTROS, verbose_name=_("Categoría"),  db_index=True)
    
    # ──────────────────────────────────────────────────────────────────────
    # CAMPOS DE MODERACIÓN Y WORKFLOW
    # ──────────────────────────────────────────────────────────────────────
    
    estado = models.CharField(max_length=20, choices=EstadoAprobacion.choices, default=EstadoAprobacion.PENDIENTE, verbose_name=_("Estado de aprobación"), db_index=True)
    motivo_rechazo = models.TextField(verbose_name=_("Motivo de rechazo"), blank=True, null=True)
    publicado = models.BooleanField(default=True, verbose_name=_("Publicado"), db_index=True)  
    
    # ──────────────────────────────────────────────────────────────────────
    # INFO
    # ──────────────────────────────────────────────────────────────────────
    
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lugares_creados", verbose_name=_("Creado por"), blank=True)    
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creación"), db_index=True)
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name=_("Última actualización"))
    
    # ──────────────────────────────────────────────────────────────────────
    # METADATOS DEL MODELO
    # ──────────────────────────────────────────────────────────────────────
    
    class Meta:
        verbose_name = _("Lugar")
        verbose_name_plural = _("Lugares")
        ordering = ["-creado_en"]  # Por defecto, más recientes primero
        indexes = [
            # Índice compuesto para búsquedas geoespaciales eficientes
            models.Index(fields=["lat", "lng"], name="idx_lugar_coords"),
            # Índice para filtros comunes en el mapa
            models.Index(fields=["categoria", "estado", "publicado"], name="idx_lugar_filtros"),
        ]
        
    # ──────────────────────────────────────────────────────────────────────
    # MÉTODOS DEL MODELO
    # ──────────────────────────────────────────────────────────────────────
    
    def __str__(self):
        """Representación en string del lugar."""
        return f"{self.nombre} ({self.get_categoria_display()})"
    
    def __repr__(self):
        """Representación técnica para debugging."""
        return f"<Lugar id={self.id} nombre='{self.nombre}' estado='{self.estado}'>"
    
    @property
    def esta_aprobado(self):
        """
        Verifica si el lugar está aprobado.
        
        Returns:
            bool: True si el estado es APROBADO, False en caso contrario
        """
        return self.estado == EstadoAprobacion.APROBADO
    
    @property
    def es_visible(self):
        """
        Verifica si el lugar es visible públicamente.
        
        Un lugar es visible si está aprobado Y publicado.
        
        Returns:
            bool: True si es visible, False en caso contrario
        """
        return self.esta_aprobado and self.publicado
    
    @property
    def tiene_coordenadas(self):
        """
        Verifica si el lugar tiene coordenadas geográficas.
        
        Returns:
            bool: True si tiene latitud y longitud, False en caso contrario
        """
        return self.lat is not None and self.lng is not None
    
    def calcular_puntuacion(self):
        """
        Calcula la puntuación total del lugar basada en votos.
        
        Returns:
            int: Suma de votos (upvotes - downvotes)
        """
        from django.db.models import Sum
        total = self.votos.aggregate(total=Sum('valor'))['total']
        return total if total is not None else 0
    
    def aprobar(self, motivo=None):
        """
        Aprueba el lugar para que sea visible en el mapa.
        
        Args:
            motivo (str, optional): Comentario sobre la aprobación
        """
        self.estado = EstadoAprobacion.APROBADO
        self.motivo_rechazo = None  # Limpiar rechazo previo
        self.save(update_fields=['estado', 'motivo_rechazo', 'actualizado_en'])
    
    def rechazar(self, motivo):
        """
        Rechaza el lugar con un motivo.
        
        Args:
            motivo (str): Razón del rechazo (obligatorio)
        
        Raises:
            ValueError: Si no se proporciona un motivo
        """
        if not motivo or not motivo.strip():
            raise ValueError("Debe proporcionar un motivo para rechazar el lugar")
        
        self.estado = EstadoAprobacion.RECHAZADO
        self.motivo_rechazo = motivo
        self.publicado = False  # Ocultar automáticamente
        self.save(update_fields=['estado', 'motivo_rechazo', 'publicado', 'actualizado_en'])
    
    def get_absolute_url(self):
        """
        Obtiene la URL canónica del lugar.
        
        Returns:
            str: URL del detalle del lugar
        """
        from django.urls import reverse
        return reverse('lugar_detalle', kwargs={'pk': self.pk})


# ============================================================================
# MODELO: FAVORITO
# ============================================================================

class Favorito(models.Model):
    """
    Relación muchos-a-muchos entre usuarios y lugares favoritos.
    
    Permite a los usuarios guardar lugares de interés para:
    - Consultarlos rápidamente
    - Recibir notificaciones de eventos cercanos
    - Crear rutas personalizadas
    
    Attributes:
        usuario (User): Usuario que guardó el favorito
        lugar (Lugar): Lugar marcado como favorito
        creado_en (datetime): Cuándo se marcó como favorito
        notas (str): Notas personales del usuario sobre el lugar
    """
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favoritos", verbose_name=_("Usuario"))
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name="favoritos", verbose_name=_("Lugar"))    
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de favorito"), help_text=_("Cuándo se marcó este lugar como favorito"))
    class Meta:
        verbose_name = _("Favorito")
        verbose_name_plural = _("Favoritos")
        unique_together = ("usuario", "lugar")         # Evita que un usuario marque el mismo lugar como favorito dos veces
        ordering = ["-creado_en"]
        indexes = [
            models.Index(fields=["usuario", "-creado_en"], name="idx_favoritos_usuario"),
        ]
    
    def __str__(self):
        return f"{self.usuario.username} → {self.lugar.nombre}"
    
    def __repr__(self):
        return f"<Favorito usuario='{self.usuario.username}' lugar='{self.lugar.nombre}'>"


# ============================================================================
# MODELO: COMENTARIO
# ============================================================================

class Comentario(models.Model):
    """
    Comentarios de usuarios sobre lugares culturales.
    
    Permite:
    - Compartir experiencias
    - Dar consejos (mejor hora para visitar, etc.)
    - Reportar problemas (cerrado temporalmente, etc.)
    
    Attributes:
        usuario (User): Autor del comentario
        lugar (Lugar): Lugar comentado
        texto (str): Contenido del comentario
        creado_en (datetime): Fecha de publicación

    """
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comentarios", verbose_name=_("Usuario"))
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name="comentarios", verbose_name=_("Lugar"))    
    texto = models.TextField(verbose_name=_("Comentario"), help_text=_("Comparte tu experiencia en este lugar"), max_length=1000)
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de publicación"))    
    class Meta:
        verbose_name = _("Comentario")
        verbose_name_plural = _("Comentarios")
        ordering = ["-creado_en"]  # Más recientes primero
        indexes = [
            # Índice para cargar comentarios de un lugar rápidamente
            models.Index(fields=["lugar", "-creado_en"], name="idx_comentarios_lugar"),
        ]          
        
    def __str__(self):
        return f"{self.usuario.username}, {self.lugar.nombre}: {self.texto}"
    
    def __repr__(self):
        return f"<Comentario id={self.id} usuario='{self.usuario.username}' lugar='{self.lugar.nombre}'>"
    
# ============================================================================
# MODELO: VOTO
# ============================================================================

class Voto(models.Model):
    """
    Sistema de votación para lugares (upvote/downvote).
    
    Permite a la comunidad:
    - Validar la calidad de lugares propuestos
    - Ordenar lugares por popularidad
    - Identificar lugares destacados
    
    Attributes:
        usuario (User): Usuario que vota
        lugar (Lugar): Lugar votado
        valor (int): Tipo de voto (1=upvote, -1=downvote)
        creado_en (datetime): Cuándo se emitió el voto
    """
    UPVOTE = 1
    DOWNVOTE = -1
    
    VOTO_CHOICES = (
        (UPVOTE, _("Útil / Me gusta")),
        (DOWNVOTE, _("No útil / No me gusta")),
    )
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votos", verbose_name=_("Usuario"))    
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name="votos", verbose_name=_("Lugar"))    
    valor = models.SmallIntegerField(choices=VOTO_CHOICES, verbose_name=_("Tipo de voto"), help_text=_("1 = upvote, -1 = downvote"))
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de voto")) 
    actualizado_en =models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de actualización de voto"))   
    class Meta:
        verbose_name = _("Voto")
        verbose_name_plural = _("Votos")
        # Un usuario solo puede votar una vez por lugar
        unique_together = ("usuario", "lugar")
        indexes = [
            # Índice para calcular puntuación de lugares eficientemente
            models.Index(fields=["lugar", "valor"], name="idx_votos_lugar"),
        ]
    
    def __str__(self):
        tipo_voto = "👍" if self.valor == self.UPVOTE else "👎"
        return f"{self.usuario.username} {tipo_voto} {self.lugar.nombre}"
    
    def __repr__(self):
        return f"<Voto usuario='{self.usuario.username}' lugar='{self.lugar.nombre}' valor={self.valor}>"
    
    def cambiar_voto(self):
        """
        Cambia el voto actual (upvote ↔ downvote).
        """
        self.valor = -self.valor
        self.save(update_fields=['valor', 'actualizado_en'])