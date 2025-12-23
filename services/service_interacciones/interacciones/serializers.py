from rest_framework import serializers
from .models import Comentario, Voto, Favorito

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['id', 'usuario_id', 'lugar_id', 'texto', 'creado_en']
        read_only_fields = ['usuario_id', 'lugar_id', 'creado_en']

class VotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voto
        fields = ['id', 'usuario_id', 'lugar_id', 'valor', 'creado_en']
        read_only_fields = ['usuario_id', 'creado_en']
        extra_kwargs = {'lugar_id': {'required': True}}

    def validate_valor(self, value):
        if value not in [1, -1]:
            raise serializers.ValidationError("El voto debe ser 1 (Upvote) o -1 (Downvote).")
        return value

class FavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorito
        fields = ['id', 'usuario_id', 'lugar_id', 'creado_en']
        read_only_fields = ['usuario_id', 'creado_en']
        extra_kwargs = {'lugar_id': {'required': True}}