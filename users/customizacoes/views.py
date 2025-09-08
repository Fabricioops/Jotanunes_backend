# customizacoes/views.py

# Views definem a lógica de como a API responde a requisições.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Importa os modelos e serializers que a view irá usar.
from .models import Customizacao, HistoricoAlteracao, Dependencia, DocumentacaoTecnica, TipoCustomizacao
from .serializers import CustomizacaoSerializer, HistoricoAlteracaoSerializer, DependenciaSerializer, DocumentacaoTecnicaSerializer, TipoCustomizacaoSerializer

# --- ViewSet para Customizacao ---
# ModelViewSet fornece automaticamente as ações de Listar, Criar, Ver, Editar e Deletar.
class CustomizacaoViewSet(viewsets.ModelViewSet):
    queryset = Customizacao.objects.all()  # O conjunto de todos os objetos que esta view pode operar.
    serializer_class = CustomizacaoSerializer # A classe serializer a ser usada.
    permission_classes = [IsAuthenticated]      # Apenas usuários autenticados podem acessar.
    
    # Configurações para filtros, busca e ordenação na API.
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'ativo']       # Campos para filtro exato (ex: /api/customizacoes/?ativo=true).
    search_fields = ['nome', 'descricao', 'codigo_erp'] # Campos para busca textual (ex: /api/customizacoes/?search=minha_formula).
    ordering_fields = ['nome', 'data_criacao'] # Campos para ordenação (ex: /api/customizacoes/?ordering=-data_criacao).

    # Este método é chamado quando uma nova customização é criada (requisição POST).
    def perform_create(self, serializer):
        # Salva o novo objeto, definindo o 'criado_por' com o usuário da requisição.
        serializer.save(criado_por=self.request.user)
        # Cria um registro no histórico para esta ação.
        HistoricoAlteracao.objects.create(
            customizacao=serializer.instance,
            alterado_por=self.request.user,
            tipo_alteracao='Criação',
            detalhes_alteracao='Customização criada inicialmente.'
        )

# --- ViewSet para HistoricoAlteracao ---
# ReadOnlyModelViewSet fornece apenas ações de leitura (Listar e Ver).
class HistoricoAlteracaoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistoricoAlteracao.objects.all().order_by('-data_alteracao') # Ordena do mais recente para o mais antigo.
    serializer_class = HistoricoAlteracaoSerializer
    permission_classes = [IsAuthenticated]

# ... (Crie ViewSets para os outros modelos: TipoCustomizacao, Dependencia, DocumentacaoTecnica)
class TipoCustomizacaoViewSet(viewsets.ModelViewSet):
    queryset = TipoCustomizacao.objects.all()
    serializer_class = TipoCustomizacaoSerializer
    permission_classes = [IsAuthenticated]

class DependenciaViewSet(viewsets.ModelViewSet):
    queryset = Dependencia.objects.all()
    serializer_class = DependenciaSerializer
    permission_classes = [IsAuthenticated]

class DocumentacaoTecnicaViewSet(viewsets.ModelViewSet):
    queryset = DocumentacaoTecnica.objects.all()
    serializer_class = DocumentacaoTecnicaSerializer
    permission_classes = [IsAuthenticated]
