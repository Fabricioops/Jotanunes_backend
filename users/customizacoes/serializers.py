# customizacoes/serializers.py

# Serializers convertem objetos do Django em JSON (para a API) e vice-versa.
from rest_framework import serializers
from .models import Customizacao, HistoricoAlteracao, Dependencia, DocumentacaoTecnica, TipoCustomizacao

# --- Serializer para TipoCustomizacao ---
class TipoCustomizacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCustomizacao  # O modelo que este serializer irá usar.
        fields = '__all__'       # Inclui todos os campos do modelo.

# --- Serializer para Customizacao ---
class CustomizacaoSerializer(serializers.ModelSerializer):
    # Campo somente leitura para mostrar o nome do tipo de customização na API.
    tipo_nome = serializers.CharField(source='tipo.nome', read_only=True)

    class Meta:
        model = Customizacao
        fields = '__all__'
        # Campos que não podem ser editados diretamente pela API.
        read_only_fields = ('data_criacao', 'data_ultima_alteracao', 'criado_por')

# --- Serializer para HistoricoAlteracao ---
class HistoricoAlteracaoSerializer(serializers.ModelSerializer):
    # Campo somente leitura para mostrar o nome de usuário de quem fez a alteração.
    alterado_por_username = serializers.CharField(source='alterado_por.username', read_only=True)

    class Meta:
        model = HistoricoAlteracao
        fields = '__all__'
        read_only_fields = ('data_alteracao',)

# ... (Crie serializers para Dependencia e DocumentacaoTecnica da mesma forma)
class DependenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependencia
        fields = '__all__'

class DocumentacaoTecnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentacaoTecnica
        fields = '__all__'
