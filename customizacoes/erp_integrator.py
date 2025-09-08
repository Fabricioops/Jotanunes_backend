# customizacoes/erp_integrator.py

import pyodbc
import os
from datetime import datetime, timedelta
from .models import Customizacao, TipoCustomizacao, HistoricoAlteracao
from django.contrib.auth import get_user_model
from .notificacao import notificar_usuario # Importa a função de notificação

User = get_user_model()

# Função para obter uma conexão com o banco de dados do ERP.
def get_erp_db_connection():
    # Lê as credenciais do banco de dados a partir das variáveis de ambiente.
    conn_str = (
        f"DRIVER={{{os.getenv('ODBC_DRIVER')}}};"
        f"SERVER={os.getenv('DB_HOST')},{os.getenv('DB_PORT')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASSWORD')};"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)

# Função para monitorar o ERP e sincronizar com o banco de dados do Django.
def monitorar_novas_customizacoes_erp():
    # Tenta encontrar um usuário administrador para receber as notificações.
    admin_user = User.objects.filter(is_superuser=True).first()

    conn = None
    try:
        conn = get_erp_db_connection()
        cursor = conn.cursor()
        
        # !!! IMPORTANTE: Adapte esta consulta para a sua realidade do ERP RM TOTVS !!!
        cursor.execute("SELECT ID_CUSTOMIZACAO, NOME, TIPO, DATA_CRIACAO FROM FCUSTOMIZACOES WHERE DATA_CRIACAO > ?", datetime.now() - timedelta(days=1))
        novas_customizacoes_erp = cursor.fetchall()

        for erp_cust in novas_customizacoes_erp:
            erp_id, nome, tipo_str, data_criacao_erp = erp_cust
            
            # Se a customização do ERP ainda não existe no nosso banco...
            if not Customizacao.objects.filter(codigo_erp=erp_id).exists():
                # ...cria ela no nosso banco.
                # (Lógica de criação da customização e do histórico)

                # E então, notifica o administrador.
                if admin_user:
                    assunto = f"[ERP] Nova Customização Detectada: {nome}"
                    mensagem = f"Uma nova customização foi detectada no ERP: '{nome}' (ID: {erp_id})."
                    notificar_usuario(admin_user, assunto, mensagem)

    except pyodbc.Error as e:
        print(f"Erro ao consultar o banco de dados do ERP: {e}")
    finally:
        if conn:
            conn.close()
