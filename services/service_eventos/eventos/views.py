from rest_framework import viewsets, permissions
from .models import Evento, EstadoEvento
from .serializers import EventoSerializer


class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all().order_by("fecha_inicio")
    serializer_class = EventoSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        usuario_id = 1

        if self.request.user and self.request.user.is_authenticated:
            usuario_id = self.request.user.id

        serializer.save(creado_por_id=usuario_id, estado=EstadoEvento.PENDIENTE)
