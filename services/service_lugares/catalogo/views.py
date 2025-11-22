from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Lugar, EstadoAprobacion
from .serializers import LugarSerializer
from .permissions import IsOrganizadorOrAdmin

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
        
    @action(detail=True, methods=['put'], permission_classes=[IsOrganizadorOrAdmin])
    def aprobar(self, request, pk=None):
        """
        Endpoint para que un Organizador apruebe un lugar.
        Ruta: PUT /api/catalogo/lugares/{pk}/aprobar/
        """
        try:
            lugar = Lugar.objects.get(pk=pk)
        except Lugar.DoesNotExist:
            return Response({'error': 'Lugar no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Cambiamos el estado
        lugar.estado = EstadoAprobacion.APROBADO
        lugar.save()

        return Response({'status': 'Lugar aprobado correctamente'}, status=status.HTTP_200_OK)