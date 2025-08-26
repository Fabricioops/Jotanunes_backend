from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Customizacao, Alerta, Historico, Dependencia
from .serializers import (
    CustomizacaoSerializer, AlertaSerializer, HistoricoSerializer, DependenciaSerializer
)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user and request.user.is_staff


class CustomizacaoViewSet(viewsets.ModelViewSet):
    queryset = Customizacao.objects.all().select_related('autor')
    serializer_class = CustomizacaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo', 'chave_registro', 'descricao', 'tipo', 'status']
    ordering_fields = ['criado_em', 'atualizado_em', 'titulo']

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def adicionar_alerta(self, request, pk=None):
        custom = self.get_object()
        data = {**request.data, 'customizacao': custom.id}
        ser = AlertaSerializer(data=data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def adicionar_historico(self, request, pk=None):
        custom = self.get_object()
        data = {**request.data, 'customizacao': custom.id, 'autor': request.user.id}
        ser = HistoricoSerializer(data=data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)


class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
    permission_classes = [IsAdminOrReadOnly]


class HistoricoViewSet(viewsets.ModelViewSet):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    permission_classes = [permissions.IsAuthenticated]


class DependenciaViewSet(viewsets.ModelViewSet):
    queryset = Dependencia.objects.all()
    serializer_class = DependenciaSerializer
    permission_classes = [permissions.IsAuthenticated]


# --------- Views HTML (Bootstrap) ---------
def dashboard(request):
    cards = {
        'total': Customizacao.objects.count(),
        'abertos': Customizacao.objects.filter(status='ABERTO').count(),
        'homolog': Customizacao.objects.filter(status='HOMOLOG').count(),
        'producao': Customizacao.objects.filter(status='PROD').count(),
    }
    recentes = Customizacao.objects.all().order_by('-atualizado_em')[:10]
    return render(request, 'customizacoes/dashboard.html', {'cards': cards, 'recentes': recentes})
