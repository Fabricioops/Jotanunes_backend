# customizacoes/notificacoes.py

import requests
from django.core.mail import send_mail
from django.conf import settings
from users.models import ConfiguracaoNotificacao # Importa o modelo de configuração

# --- Função para Enviar Notificação para Microsoft Teams ---
def enviar_notificacao_teams(webhook_url, titulo, mensagem):
    payload = {
        "@type": "MessageCard",
        "summary": titulo,
        "sections": [{"activityTitle": titulo, "activitySubtitle": mensagem, "markdown": True}]
    }
    try:
        requests.post(webhook_url, json=payload).raise_for_status()
        print(f"Notificação do Teams enviada com sucesso.")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar notificação para o Teams: {e}")

# ... (Crie funções similares para Slack e E-mail)

# --- Função Principal para Notificar o Usuário ---
# Orquestra o envio de notificações para um usuário, verificando suas preferências.
def notificar_usuario(usuario, assunto, mensagem):
    try:
        config = usuario.config_notificacao
    except ConfiguracaoNotificacao.DoesNotExist:
        # Se o usuário não tem configuração, não faz nada ou cria uma padrão.
        return

    # Enviar E-mail (se configurado)
    if config.receber_email and config.email_para_notificacao:
        send_mail(assunto, mensagem, settings.DEFAULT_FROM_EMAIL, [config.email_para_notificacao])

    # Enviar para Microsoft Teams (se configurado)
    if config.webhook_teams:
        enviar_notificacao_teams(config.webhook_teams, assunto, mensagem)

    # Enviar para Slack (se configurado)
    if config.webhook_slack:
        # (implementar a função enviar_notificacao_slack)
        pass
