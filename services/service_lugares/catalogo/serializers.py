from rest_framework import serializers
from .models import Lugar

class LugarSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='get_categoria_display', read_only=True)
    estado_nombre = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = Lugar
        fields = [
            'id', 'nombre', 'descripcion', 'direccion', 
            'lat', 'lng', 'categoria', 'categoria_nombre',
            'estado', 'estado_nombre', 'creado_por_id', 
            'creado_en', 'esta_aprobado'
        ]
        read_only_fields = [
            'estado', 'estado_nombre', 'creado_por_id', 
            'creado_en', 'esta_aprobado'
        ]