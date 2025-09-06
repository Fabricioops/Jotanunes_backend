# users/models.py (ou notificacoes/models.py)armazenar as configurações de notificação de cada usuário
# users/models.py (ou notificacoes/models.py)

from django.db import models
from django.contrib.auth import get_user_model

# Obtém o modelo de usuário ativo no projeto. Essencial para criar a relação com o usuário.
User = get_user_model()

# --- Modelo ConfiguracaoNotificacao ---
# Este modelo armazena as preferências de notificação para cada usuário.
class ConfiguracaoNotificacao(models.Model):
    # models.OneToOneField: Cria uma relação de "um para um" com o modelo User.
    # Isso significa que cada usuário pode ter APENAS UMA configuração de notificação,
    # e cada configuração pertence a APENAS UM usuário.
    # on_delete=models.CASCADE: Se o usuário for deletado, sua configuração de notificação também será.
    # related_name="config_notificacao": Permite acessar a configuração de um usuário com `usuario.config_notificacao`.
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="config_notificacao")
    
    # models.BooleanField: Campo booleano (True/False) para indicar se o usuário deseja receber e-mails.
    # default=True: Por padrão, o usuário receberá e-mails.
    receber_email = models.BooleanField(default=True)
    
    # models.EmailField: Campo para armazenar um endereço de e-mail.
    # blank=True, null=True: Torna este campo opcional.
    email_para_notificacao = models.EmailField(blank=True, null=True)
    
    # models.URLField: Campo para armazenar uma URL (endereço web).
    # blank=True, null=True: Torna este campo opcional.
    # help_text: Texto de ajuda para o usuário no painel de administração.
    webhook_teams = models.URLField(blank=True, null=True, help_text="URL do Webhook do Microsoft Teams")
    
    # models.URLField: Campo para armazenar uma URL para o webhook do Slack.
    webhook_slack = models.URLField(blank=True, null=True, help_text="URL do Webhook do Slack")

    # Define a representação em texto do objeto ConfiguracaoNotificacao.
    def __str__(self):
        return f"Configurações de Notificação para {self.usuario.username}"


