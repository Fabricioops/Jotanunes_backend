# users/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# --- Modelo ConfiguracaoNotificacao ---
# Armazena as preferências de notificação para cada usuário.
class ConfiguracaoNotificacao(models.Model):
    # models.OneToOneField: Relação de "um para um" com o modelo User.
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="config_notificacao")
    # Campo booleano (True/False) para indicar se o usuário deseja receber e-mails.
    receber_email = models.BooleanField(default=True)
    # Campo para armazenar um endereço de e-mail opcional.
    email_para_notificacao = models.EmailField(blank=True, null=True)
    # Campo para armazenar a URL do webhook do Microsoft Teams.
    webhook_teams = models.URLField(blank=True, null=True, help_text="URL do Webhook do Microsoft Teams")
    # Campo para armazenar a URL do webhook do Slack.
    webhook_slack = models.URLField(blank=True, null=True, help_text="URL do Webhook do Slack")

    def __str__(self):
        return f"Configurações de Notificação para {self.usuario.username}"
