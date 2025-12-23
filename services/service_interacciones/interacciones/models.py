from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Favorito(models.Model):
    usuario_id = models.IntegerField(db_index=True)
    lugar_id = models.IntegerField(db_index=True, null=True, blank=True)
    evento_id = models.IntegerField(db_index=True, null=True, blank=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Favorito")
        verbose_name_plural = _("Favoritos")
        ordering = ["-creado_en"]
        # Evitar duplicados: Un usuario solo puede marcar una vez un lugar O un evento
        constraints = [
            models.UniqueConstraint(fields=['usuario_id', 'lugar_id'], name='unique_fav_lugar'),
            models.UniqueConstraint(fields=['usuario_id', 'evento_id'], name='unique_fav_evento')
        ]

    def save(self, *args, **kwargs):
        if not self.lugar_id and not self.evento_id:
            raise ValidationError("Debe especificar un lugar_id o un evento_id.")
        if self.lugar_id and self.evento_id:
            raise ValidationError("No puede ser favorito de lugar y evento a la vez.")
        super().save(*args, **kwargs)

class Comentario(models.Model):
    usuario_id = models.IntegerField(db_index=True)
    lugar_id = models.IntegerField(db_index=True, null=True, blank=True)
    evento_id = models.IntegerField(db_index=True, null=True, blank=True)
    
    texto = models.TextField(max_length=1000)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Comentario")
        verbose_name_plural = _("Comentarios")
        ordering = ["-creado_en"]

class Voto(models.Model):
    # Validaremos en el serializer que sea entre 1 y 5
    usuario_id = models.IntegerField(db_index=True)
    lugar_id = models.IntegerField(db_index=True, null=True, blank=True)
    evento_id = models.IntegerField(db_index=True, null=True, blank=True)
    
    valor = models.SmallIntegerField() # 1 a 5 estrellas
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Voto")
        verbose_name_plural = _("Votos")
        constraints = [
            models.UniqueConstraint(fields=['usuario_id', 'lugar_id'], name='unique_voto_lugar'),
            models.UniqueConstraint(fields=['usuario_id', 'evento_id'], name='unique_voto_evento')
        ]