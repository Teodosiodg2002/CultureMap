from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Lugar, EstadoAprobacion
from .serializers import LugarSerializer
from .permissions import IsOrganizadorOrAdmin

class LugarViewSet(viewsets.ModelViewSet):
    serializer_class = LugarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        rol = getattr(user, 'rol', None)
        
        if user.is_authenticated and rol in ['admin', 'organizador']:
            return Lugar.objects.all().order_by('-creado_en')
        
        return Lugar.objects.filter(estado=EstadoAprobacion.APROBADO, publicado=True).order_by('-creado_en')

    def perform_create(self, serializer):
        usuario_id = 1
        if self.request.user and self.request.user.is_authenticated:
            usuario_id = self.request.user.id
            
        serializer.save(
            creado_por_id=usuario_id,
            estado=EstadoAprobacion.PENDIENTE
        )

    # --- ACCIONES DE MODERACIÓN ---
    @action(detail=True, methods=['put'], permission_classes=[IsOrganizadorOrAdmin])
    def aprobar(self, request, pk=None):
        lugar = self.get_object()
        lugar.estado = EstadoAprobacion.APROBADO
        lugar.publicado = True
        lugar.save()
        return Response({'status': 'Lugar aprobado'})

    @action(detail=True, methods=['put'], permission_classes=[IsOrganizadorOrAdmin])
    def rechazar(self, request, pk=None):
        lugar = self.get_object()
        lugar.estado = EstadoAprobacion.RECHAZADO
        lugar.publicado = False
        lugar.save()
        return Response({'status': 'Lugar rechazado'})