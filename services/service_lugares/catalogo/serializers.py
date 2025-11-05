# services/service_lugares/catalogo/serializers.py

from rest_framework import serializers
from .models import Lugar, Categoria, EstadoAprobacion

class LugarSerializer(serializers.ModelSerializer):
    """
    Este 'traductor' convierte el modelo Lugar a JSON
    y valida los datos de entrada.
    """

    categoria_nombre = serializers.CharField(source='get_categoria_display', read_only=True)
    estado_nombre = serializers.CharField(source='get_estado_display', read_only=True)

    esta_aprobado = serializers.ReadOnlyField()
    es_visible = serializers.ReadOnlyField()

    class Meta:
        model = Lugar
        fields = [
            'id', 
            'nombre', 
            'descripcion', 
            'direccion', 
            'lat', 
            'lng', 
            'categoria',            
            'categoria_nombre',     
            'estado',               
            'estado_nombre',        
            'creado_por_id',        # El ID del usuario que lo creó
            'creado_en',
            'esta_aprobado',
            'es_visible',
        ]

        # --- Campos de Solo Lectura (para la salida) ---
        read_only_fields = [
            'estado',
            'estado_nombre',
            'creado_por_id',
            'creado_en',
            'esta_aprobado',
            'es_visible',
        ]