from rest_framework import serializers
from .models import Comentario, Voto

# --- Serializador para Comentarios ---

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['id', 'usuario_id', 'lugar_id', 'texto', 'creado_en']
        read_only_fields = ['usuario_id', 'lugar_id', 'creado_en']

# --- Serializador para Votos ---

class VotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voto
        fields = ['id', 'usuario_id', 'lugar_id', 'valor', 'creado_en']
        
        read_only_fields = ['usuario_id', 'creado_en']

    def validate_valor(self, value):
        """
        Validación extra para asegurar que el valor es 1 o -1,
        aunque el modelo ya tiene 'choices', esto da un mensaje más limpio.
        """
        if value not in [1, -1]:
            raise serializers.ValidationError("El voto debe ser 1 (Upvote) o -1 (Downvote).")
        return value