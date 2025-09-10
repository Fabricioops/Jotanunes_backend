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


# --- Função para Enviar E-mail ---

def enviar_notificacao_email(destinatario, assunto, mensagem):
    try:
        # send_mail(): Função do Django para enviar e-mails.
        # Ela usa as configurações definidas em settings.py (que por sua vez lê do .env).
        send_mail(assunto, mensagem, settings.DEFAULT_FROM_EMAIL, [destinatario])
        print(f"E-mail enviado para {destinatario}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# --- Função para Enviar Notificação para Slack ---------------------------------
# webhook_url: A URL do webhook do Slack para onde a mensagem será enviada.
# titulo: O título da notificação.
# mensagem: O corpo da mensagem.
def enviar_notificacao_slack(webhook_url, titulo, mensagem):
    # payload: O dicionário de dados que será enviado para o webhook do Slack.
    # O Slack espera um campo "text" para o conteúdo da mensagem.
    payload = {
        "text": f"*{titulo}*\n{mensagem}" # Formata a mensagem com o título em negrito e quebra de linha.
    }
    try:
        # requests.post(): Envia uma requisição POST HTTP para a URL do webhook com o payload JSON.
        # .raise_for_status(): Verifica se a requisição foi bem-sucedida.
        requests.post(webhook_url, json=payload).raise_for_status() 
        print(f"Notificação do Slack enviada com sucesso para {webhook_url}")
    except requests.exceptions.RequestException as e:
        # Captura erros relacionados à requisição HTTP e os imprime.
        print(f"Erro ao enviar notificação para o Slack ({webhook_url}): {e}")


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
        # (implementar a função enviar_notificacao_slack) #complete aqui 
        pass
