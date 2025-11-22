from rest_framework import serializers
from .models import Evento

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'
        read_only_fields = ['estado', 'creado_por_id', 'creado_en']