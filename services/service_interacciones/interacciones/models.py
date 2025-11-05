# services/service_interacciones/interacciones/models.py

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# ============================================================================
# MODELO: FAVORITO
# ============================================================================

class Favorito(models.Model):

    usuario_id = models.IntegerField(db_index=True)
    lugar_id = models.IntegerField(db_index=True)

    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Favorito")
        verbose_name_plural = _("Favoritos")
        unique_together = ("usuario_id", "lugar_id")
        ordering = ["-creado_en"]

# ============================================================================
# MODELO: COMENTARIO
# ============================================================================

class Comentario(models.Model):

    usuario_id = models.IntegerField(db_index=True)
    lugar_id = models.IntegerField(db_index=True)

    texto = models.TextField(max_length=1000)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Comentario")
        verbose_name_plural = _("Comentarios")
        ordering = ["-creado_en"]

# ============================================================================
# MODELO: VOTO
# ============================================================================

class Voto(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1
    VOTO_CHOICES = (
        (UPVOTE, _("Upvote")),
        (DOWNVOTE, _("Downvote")),
    )

    usuario_id = models.IntegerField(db_index=True)
    lugar_id = models.IntegerField(db_index=True)

    valor = models.SmallIntegerField(choices=VOTO_CHOICES)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Voto")
        verbose_name_plural = _("Votos")
        unique_together = ("usuario_id", "lugar_id")