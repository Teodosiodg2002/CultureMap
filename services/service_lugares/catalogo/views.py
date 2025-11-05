from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Lugar, EstadoAprobacion
from .serializers import LugarSerializer

class LugarViewSet(viewsets.ModelViewSet):
    """
    Este ViewSet proporciona automáticamente las acciones
    `list` (listar), `create` (crear), `retrieve` (detalle),
    `update` (actualizar) y `destroy` (borrar) para el modelo Lugar.
    """

    serializer_class = LugarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Esta función define qué lugares se devuelven.
        """
        return Lugar.objects.filter(
            estado=EstadoAprobacion.APROBADO,
            publicado=True
        ).order_by('-creado_en')

    def perform_create(self, serializer):
        """
        Sobreescribimos este método para asignar automáticamente el 'creado_por_id'
        y el 'estado' al crear un nuevo lugar a través de la API.
        """
        serializer.save(
            creado_por_id=self.request.user.id,
            estado=EstadoAprobacion.PENDIENTE
        )