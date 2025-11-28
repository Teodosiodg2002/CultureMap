from rest_framework import viewsets, permissions, status
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
        """
        Filtrar eventos:
        - Si es Admin/Organizador: Ve TODOS (para poder aprobarlos).
        - Si es Usuario/Anónimo: Ve SOLO los PUBLICADOS.
        """
        user = self.request.user
        rol = getattr(user, 'rol', None)

        if user.is_authenticated and rol in ['admin', 'organizador']:
            return Evento.objects.all().order_by('fecha_inicio')
        
        # Público general: Solo publicados
        return Evento.objects.filter(estado=EstadoEvento.PUBLICADO).order_by('fecha_inicio')

    def perform_create(self, serializer):
        usuario_id = 1
        if self.request.user and self.request.user.is_authenticated:
            usuario_id = self.request.user.id
            
        serializer.save(
            creado_por_id=usuario_id,
            estado=EstadoEvento.PENDIENTE
        )

    @action(detail=True, methods=['put'], permission_classes=[IsOrganizadorOrAdmin])
    def aprobar(self, request, pk=None):
        evento = self.get_object()
        evento.estado = EstadoEvento.PUBLICADO # O 'aprobado' según tu modelo
        evento.save()
        return Response({'status': 'Evento aprobado'})

    @action(detail=True, methods=['put'], permission_classes=[IsOrganizadorOrAdmin])
    def rechazar(self, request, pk=None):
        evento = self.get_object()
        evento.estado = EstadoEvento.CANCELADO # O 'rechazado' según tu modelo
        evento.save()
        return Response({'status': 'Evento rechazado'})