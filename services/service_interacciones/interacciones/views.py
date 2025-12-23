from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .models import Comentario, Voto, Favorito
from .serializers import ComentarioSerializer, VotoSerializer, FavoritoSerializer

# --- COMENTARIOS ---

class ComentarioListCreateView(generics.ListCreateAPIView):
    serializer_class = ComentarioSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comentario.objects.filter(lugar_id=self.kwargs['lugar_id']).order_by('-creado_en')

    def perform_create(self, serializer):
        serializer.save(usuario_id=self.request.user.id, lugar_id=self.kwargs['lugar_id'])


# --- VOTOS ---

class VotoUpsertView(generics.GenericAPIView):
    """Crea o actualiza un voto (Upsert)"""
    serializer_class = VotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
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


# --- FAVORITOS ---

class FavoritoToggleView(views.APIView):
    """Acción de 'Me gusta' / 'Ya no me gusta' (Toggle)"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        lugar_id = request.data.get('lugar_id')
        if not lugar_id:
            return Response({'error': 'lugar_id requerido'}, status=status.HTTP_400_BAD_REQUEST)

        # Si existe, lo borramos (Ya no me gusta). Si no, lo creamos.
        favorito, created = Favorito.objects.get_or_create(
            usuario_id=request.user.id,
            lugar_id=lugar_id
        )

        if not created:
            favorito.delete()
            return Response({'status': 'eliminado', 'lugar_id': lugar_id}, status=status.HTTP_200_OK)
        
        return Response({'status': 'creado', 'lugar_id': lugar_id}, status=status.HTTP_201_CREATED)

class FavoritoListView(generics.ListAPIView):
    """Lista todos los favoritos del usuario actual"""
    serializer_class = FavoritoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorito.objects.filter(usuario_id=self.request.user.id)