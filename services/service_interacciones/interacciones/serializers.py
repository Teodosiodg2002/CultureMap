from rest_framework import serializers
from .models import Comentario, Voto, Favorito

# --- Serializer para Comentarios ---
class ComentarioSerializer(serializers.ModelSerializer):
    """
    Traductor para el modelo Comentario.
    El usuario solo necesita enviar el campo 'texto'.
    """
    class Meta:
        model = Comentario
        fields = [
            'id', 
            'lugar_id',     
            'usuario_id',  
            'texto',      
            'creado_en'
        ]
        read_only_fields = ['lugar_id', 'usuario_id', 'creado_en']

# --- Serializer para Votos ---
class VotoSerializer(serializers.ModelSerializer):
    """
    Traductor para el modelo Voto.
    El usuario solo necesita enviar el campo 'valor' (1 o -1).
    """
    class Meta:
        model = Voto
        fields = [
            'id', 
            'lugar_id', 
            'usuario_id', 
            'valor',
            'creado_en'
        ]
        read_only_fields = ['usuario_id', 'creado_en']

# --- Serializer para Favoritos ---
class FavoritoSerializer(serializers.ModelSerializer):
    """
    Traductor para el modelo Favorito.
    Este serializer no necesita campos de entrada, solo de salida.
    """
    class Meta:
        model = Favorito
        fields = ['id', 'lugar_id', 'usuario_id', 'creado_en']
        read_only_fields = ['lugar_id', 'usuario_id', 'creado_en']