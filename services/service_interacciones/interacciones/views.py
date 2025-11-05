from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Comentario, Voto
from .serializers import ComentarioSerializer, VotoSerializer

# --- Vista para Comentarios (Listar y Crear) ---

class ComentarioListCreateView(generics.ListCreateAPIView):
    """
    API View para:
    - GET: Listar todos los comentarios de un lugar específico.
    - POST: Crear un nuevo comentario para un lugar específico.

    La URL contendrá el ID del lugar (ej: /api/lugar/5/comentarios/)
    """
    serializer_class = ComentarioSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Filtra los comentarios para que solo devuelva
        los del 'lugar_id' especificado en la URL.
        """
        lugar_id = self.kwargs['lugar_id']
        return Comentario.objects.filter(lugar_id=lugar_id).order_by('-creado_en')

    def perform_create(self, serializer):
        """
        Asigna automáticamente el 'usuario_id' (del token)
        y el 'lugar_id' (de la URL) al crear un comentario.
        """
        lugar_id = self.kwargs['lugar_id']
        serializer.save(usuario_id=self.request.user.id, lugar_id=lugar_id)


# --- Vista para Votos (Crear y Actualizar) ---

class VotoCreateUpdateView(generics.CreateAPIView):
    """
    API View para:
    - POST: Crear o Actualizar un voto para un lugar.

    La URL será genérica (ej: /api/interacciones/votar/)
    El 'lugar_id' y el 'valor' vendrán en el body del JSON.
    """
    serializer_class = VotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Sobreescribimos el método 'create' para implementar
        la lógica de "votar una sola vez" (Upsert).
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lugar_id = serializer.validated_data['lugar_id']
        valor = serializer.validated_data['valor']

        voto, created = Voto.objects.update_or_create(
            usuario_id=request.user.id,  
            lugar_id=lugar_id,            
            defaults={'valor': valor}  
        )

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(VotoSerializer(voto).data, status=status_code)