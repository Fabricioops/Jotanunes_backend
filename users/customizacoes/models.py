# customizacoes/models.py

# Importa as bibliotecas necessárias do Django.
from django.db import models
from django.contrib.auth import get_user_model

# Obtém o modelo de usuário que está ativo no seu projeto.
User = get_user_model()

# --- Modelo TipoCustomizacao ---
# Armazena os tipos de customização que existem (ex: 'Fórmula Visual', 'Consulta SQL').
class TipoCustomizacao(models.Model):
    # models.CharField: Um campo para armazenar texto.
    # unique=True: Garante que não haverá dois tipos com o mesmo nome.
    nome = models.CharField(max_length=100, unique=True)
    # models.TextField: Um campo para textos longos, opcional.
    descricao = models.TextField(blank=True, null=True)

    # Define como o objeto será exibido (ex: no painel de administração).
    def __str__(self):
        return self.nome

# --- Modelo Customizacao ---
# O modelo principal, que representa uma customização do ERP.
class Customizacao(models.Model):
    # models.CharField: Campo de texto para o nome da customização.
    nome = models.CharField(max_length=255)
    # models.ForeignKey: Cria uma relação com o modelo TipoCustomizacao.
    # on_delete=models.SET_NULL: Se um tipo for deletado, este campo ficará nulo.
    tipo = models.ForeignKey(TipoCustomizacao, on_delete=models.SET_NULL, null=True)
    # models.CharField: Armazena o código único da customização no ERP.
    codigo_erp = models.CharField(max_length=100, unique=True, help_text="Código da customização no ERP RM TOTVS")
    # models.TextField: Descrição opcional da customização.
    descricao = models.TextField(blank=True, null=True)
    # models.DateTimeField: Armazena data e hora.
    # auto_now_add=True: Preenchido automaticamente na criação.
    data_criacao = models.DateTimeField(auto_now_add=True)
    # auto_now=True: Atualizado automaticamente a cada edição.
    data_ultima_alteracao = models.DateTimeField(auto_now=True)
    # models.ForeignKey: Relação com o usuário que criou a customização.
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='customizacoes_criadas')
    # models.BooleanField: Campo para armazenar um valor verdadeiro/falso (True/False).
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

# --- Modelo HistoricoAlteracao ---
# Armazena um registro de cada mudança feita em uma customização.
class HistoricoAlteracao(models.Model):
    # models.ForeignKey: Relação com a customização que foi alterada.
    # on_delete=models.CASCADE: Se a customização for deletada, seu histórico também será.
    customizacao = models.ForeignKey(Customizacao, on_delete=models.CASCADE, related_name='historicos')
    # models.DateTimeField: Data e hora em que a alteração foi registrada.
    data_alteracao = models.DateTimeField(auto_now_add=True)
    # models.ForeignKey: Usuário que realizou a alteração.
    alterado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # models.CharField: Tipo da alteração (ex: 'Criação', 'Edição').
    tipo_alteracao = models.CharField(max_length=50)
    # models.TextField: Descrição detalhada do que foi alterado.
    detalhes_alteracao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Alteração em {self.customizacao.nome} por {self.alterado_por.username if self.alterado_por else 'Desconhecido'}"

# --- Modelo Dependencia ---
# Mapeia as dependências entre customizações.
class Dependencia(models.Model):
    # A customização que depende de outra.
    customizacao_origem = models.ForeignKey(Customizacao, on_delete=models.CASCADE, related_name='dependencias_saida')
    # A customização da qual a origem depende.
    customizacao_destino = models.ForeignKey(Customizacao, on_delete=models.CASCADE, related_name='dependencias_entrada')
    # O tipo de dependência (ex: 'Usa', 'Referencia').
    tipo_dependencia = models.CharField(max_length=100)
    # Descrição opcional da dependência.
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        # Garante que não haverá duas dependências idênticas.
        unique_together = ('customizacao_origem', 'customizacao_destino')

    def __str__(self):
        return f"{self.customizacao_origem.nome} -> {self.customizacao_destino.nome}"

# --- Modelo DocumentacaoTecnica ---
# Armazena a documentação técnica de uma customização.
class DocumentacaoTecnica(models.Model):
    # models.OneToOneField: Relação de "um para um". Cada customização tem apenas uma documentação.
    customizacao = models.OneToOneField(Customizacao, on_delete=models.CASCADE, related_name='documentacao')
    # O conteúdo da documentação.
    conteudo = models.TextField()
    # Data e hora da última atualização.
    data_ultima_atualizacao = models.DateTimeField(auto_now=True)
    # Usuário que atualizou pela última vez.
    atualizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Documentação de {self.customizacao.nome}"
