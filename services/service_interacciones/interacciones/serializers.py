from rest_framework import serializers
from .models import Comentario, Voto, Favorito

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['id', 'usuario_id', 'lugar_id', 'evento_id', 'texto', 'creado_en']
        read_only_fields = ['usuario_id', 'creado_en']

class VotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voto
        fields = ['id', 'usuario_id', 'lugar_id', 'evento_id', 'valor', 'creado_en']
        read_only_fields = ['usuario_id', 'creado_en']

    def validate_valor(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("La valoración debe ser entre 1 y 5 estrellas.")
        return value
    
    def validate(self, data):
        lugar = data.get('lugar_id')
        evento = data.get('evento_id')
        if not lugar and not evento:
            raise serializers.ValidationError("Debes votar un lugar o un evento.")
        if lugar and evento:
            raise serializers.ValidationError("No puedes votar ambos a la vez.")
        return data

class FavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorito
        fields = ['id', 'usuario_id', 'lugar_id', 'evento_id', 'creado_en']
        read_only_fields = ['usuario_id', 'creado_en']