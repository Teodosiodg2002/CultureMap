from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .models import Comentario, Voto, Favorito
from .serializers import ComentarioSerializer, VotoSerializer, FavoritoSerializer
from django.db.models import Avg, Count

# --- COMENTARIOS ---
class ComentarioListCreateView(generics.ListCreateAPIView):
    serializer_class = ComentarioSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Detectamos si piden comentarios de lugar o evento por los query params
        lugar_id = self.kwargs.get('lugar_id')
        evento_id = self.kwargs.get('evento_id')
        
        if lugar_id:
            return Comentario.objects.filter(lugar_id=lugar_id).order_by('-creado_en')
        elif evento_id:
            return Comentario.objects.filter(evento_id=evento_id).order_by('-creado_en')
        return Comentario.objects.none()

    def perform_create(self, serializer):
        lugar_id = self.kwargs.get('lugar_id')
        evento_id = self.kwargs.get('evento_id')
        serializer.save(usuario_id=self.request.user.id, lugar_id=lugar_id, evento_id=evento_id)

# --- VOTOS (UPSERT) ---
class VotoUpsertView(generics.GenericAPIView):
    serializer_class = VotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Permitimos enviar data parcial, el serializer valida la lógica
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lugar_id = serializer.validated_data.get('lugar_id')
        evento_id = serializer.validated_data.get('evento_id')
        valor = serializer.validated_data['valor']
        
        # Lógica dinámica para update_or_create
        filtros = {'usuario_id': request.user.id}
        if lugar_id:
            filtros['lugar_id'] = lugar_id
            # Aseguramos que el otro sea null
            defaults = {'valor': valor, 'evento_id': None}
        else:
            filtros['evento_id'] = evento_id
            defaults = {'valor': valor, 'lugar_id': None}

        voto, created = Voto.objects.update_or_create(
            defaults=defaults,
            **filtros
        )
        
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(VotoSerializer(voto).data, status=status_code)

# --- FAVORITOS ---
class FavoritoToggleView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        lugar_id = request.data.get('lugar_id')
        evento_id = request.data.get('evento_id')

        if not lugar_id and not evento_id:
            return Response({'error': 'ID requerido'}, status=status.HTTP_400_BAD_REQUEST)

        # Construir filtros dinámicos
        filtros = {'usuario_id': request.user.id}
        if lugar_id: filtros['lugar_id'] = lugar_id
        if evento_id: filtros['evento_id'] = evento_id

        favorito, created = Favorito.objects.get_or_create(**filtros)

        if not created:
            favorito.delete()
            return Response({'status': 'eliminado'}, status=status.HTTP_200_OK)
        
        return Response({'status': 'creado'}, status=status.HTTP_201_CREATED)

class FavoritoListView(generics.ListAPIView):
    serializer_class = FavoritoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorito.objects.filter(usuario_id=self.request.user.id)
    
class VotoListView(generics.ListAPIView):
    """Devuelve los votos del usuario actual"""
    serializer_class = VotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Voto.objects.filter(usuario_id=self.request.user.id)

class VotoResumenView(views.APIView):
    """Devuelve la nota media y el total de votos de un recurso"""
    permission_classes = [permissions.AllowAny]

    def get(self, request, tipo, pk):
        from django.db.models import Avg, Count # Importación local por si acaso
        
        filtros = {}
        if tipo == 'lugar':
            filtros['lugar_id'] = pk
        elif tipo == 'evento':
            filtros['evento_id'] = pk
        else:
            return Response({'error': 'Tipo inválido'}, status=400)

        datos = Voto.objects.filter(**filtros).aggregate(
            media=Avg('valor'),
            total=Count('id')
        )

        return Response({
            'media': round(datos['media'], 1) if datos['media'] else 0,
            'total': datos['total']
        })