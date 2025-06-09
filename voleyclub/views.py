from django.shortcuts import render


from rest_framework import viewsets, filters
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Jugador, Pago, Categoria, Entrenador, Usuario
from .serializers import JugadorSerializer, PagoSerializer, CategoriaSerializer

#Vistas para el API

class JugadorViewSet(viewsets.ModelViewSet):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Jugador.objects.all()
    def perform_create(self, serializer):
        Usuario = self.request.user
        if Usuario.rol == 'entrenador':
            try:
                entrenador = Entrenador.objects.get(usuario=Usuario)
                serializer.save(entrenador=entrenador)
            except Entrenador.DoesNotExist:
                raise serializers.ValidationError("No se encontró un entrenador asociado a este usuario.")
        else:
            raise serializers.ValidationError("Solo los entrenadores pueden registrar jugadores.")

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['jugador', 'mes_correspondiente','concepto', 'estado']
    search_fields = ['jugador__nombre_completo']
    ordering_fields = ['fecha_pago', 'monto']

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class YoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        data = {
            'id': user.id,
            'username': user.username,
            'rol': user.rol,
            'email': user.email,
            'nombre_completo': None,
            'foto': None,
        }

        if user.rol == 'entrenador':
            try:
                entrenador = user.entrenador
                data['nombre_completo'] = entrenador.nombre_completo
                if entrenador.foto:
                    data['foto'] = entrenador.foto.url
            except Entrenador.DoesNotExist:
                pass

        return Response(data)


class JugadorFiltradoViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def mis_jugadores(self, request):
        usuario = request.user

        if usuario.rol == 'admin':
            jugadores = Jugador.objects.all()
        
        else:
            jugadores = Jugador.objects.filter(entrenador__usuario=usuario)
        
        serializer = JugadorSerializer(jugadores, many=True)
        return Response(serializer.data)