from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Evento, EstadoEvento
from .serializers import EventoSerializer
from .permissions import IsOrganizadorOrAdmin

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        rol = getattr(user, 'rol', None)

        if user.is_authenticated and rol in ['admin', 'organizador']:
            return Evento.objects.all().order_by('fecha_inicio')
        
        return Evento.objects.filter(estado=EstadoEvento.PUBLICADO).order_by('fecha_inicio')

    def perform_create(self, serializer):
        serializer.save(
            creado_por_id=self.request.user.id if self.request.user.is_authenticated else 1,
            estado=EstadoEvento.PENDIENTE
        )

    @action(detail=True, methods=['put'], permission_classes=[IsOrganizadorOrAdmin])
    def aprobar(self, request, pk=None):
        evento = self.get_object()
        evento.estado = EstadoEvento.PUBLICADO
        evento.save()
        return Response({'status': 'Evento aprobado'})

    @action(detail=True, methods=['put'], permission_classes=[IsOrganizadorOrAdmin])
    def rechazar(self, request, pk=None):
        evento = self.get_object()
        evento.estado = EstadoEvento.CANCELADO
        evento.save()
        return Response({'status': 'Evento rechazado'})