# Este arquivo centraliza a lógica de comunicação com o banco de dados do ERP RM TOTVS.
# É uma boa prática separar essa lógica para manter o código organizado.

import pyodbc  # Biblioteca para conectar a bancos de dados via ODBC.
import os      # Biblioteca para acessar variáveis de ambiente.
from datetime import datetime, timedelta # Bibliotecas para trabalhar com datas e horas.

# Função para obter uma conexão com o banco de dados do ERP.
def get_erp_db_connection():
    # Lê as credenciais do banco de dados a partir das variáveis de ambiente.
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    odbc_driver = os.getenv('ODBC_DRIVER')

    # Monta a string de conexão ODBC.
    conn_str = (
        f"DRIVER={{{odbc_driver}}};"
        f"SERVER={db_host},{db_port};"
        f"DATABASE={db_name};"
        f"UID={db_user};"
        f"PWD={db_password};"
        "TrustServerCertificate=yes;" # Necessário para algumas configurações de SQL Server.
    )
    # Retorna o objeto de conexão.
    return pyodbc.connect(conn_str)

# Função para monitorar o ERP e sincronizar com o banco de dados do Django.
def monitorar_novas_customizacoes_erp():
    # Esta função é um EXEMPLO. Você precisará adaptá-la à estrutura real do seu banco de dados ERP.
    
    # Importa os modelos do Django aqui dentro da função para evitar importações circulares.
    from customizacoes.models import Customizacao, TipoCustomizacao, HistoricoAlteracao
    from django.contrib.auth import get_user_model
    User = get_user_model()

    # Tenta obter um usuário 'sistema' para registrar alterações automáticas.
    # Se não existir, cria um. Você precisa definir uma senha segura.
    try:
        sistema_user = User.objects.get(username='sistema')
    except User.DoesNotExist:
        sistema_user = User.objects.create_user(username='sistema', password='senha_segura_aqui', is_staff=True)

    conn = None # Inicializa a variável de conexão como nula.
    try:
        # Obtém a conexão com o banco do ERP.
        conn = get_erp_db_connection()
        cursor = conn.cursor() # Cria um cursor para executar comandos SQL.
        
        # !!! IMPORTANTE: Adapte esta consulta para a sua realidade do ERP RM TOTVS !!!
        # Esta consulta de exemplo busca customizações criadas no último dia.
        # Você precisa saber o nome da tabela e das colunas no seu ERP.
        cursor.execute("SELECT ID_CUSTOMIZACAO, NOME, TIPO, DATA_CRIACAO FROM FCUSTOMIZACOES WHERE DATA_CRIACAO > ?", datetime.now() - timedelta(days=1))
        
        # Pega todos os resultados da consulta.
        novas_customizacoes_erp = cursor.fetchall()

        # Itera sobre cada customização encontrada no ERP.
        for erp_cust in novas_customizacoes_erp:
            erp_id, nome, tipo_str, data_criacao_erp = erp_cust
            
            # Verifica se a customização do ERP já existe no banco de dados do Django.
            if not Customizacao.objects.filter(codigo_erp=erp_id).exists():
                # Se não existe, vamos criá-la.
                
                # Cria ou obtém o tipo de customização.
                tipo_customizacao, created = TipoCustomizacao.objects.get_or_create(nome=tipo_str)

                # Cria a customização no banco de dados do Django.
                customizacao_django = Customizacao.objects.create(
                    nome=nome,
                    tipo=tipo_customizacao,
                    codigo_erp=erp_id,
                    data_criacao=data_criacao_erp, # Usa a data do ERP.
                    criado_por=sistema_user # Atribui ao usuário 'sistema'.
                )
                # Cria um registro de histórico para esta nova customização.
                HistoricoAlteracao.objects.create(
                    customizacao=customizacao_django,
                    alterado_por=sistema_user,
                    tipo_alteracao='Criação (ERP)',
                    detalhes_alteracao=f'Nova customização detectada no ERP: {nome} (ID: {erp_id})'
                )
                print(f"Nova customização do ERP registrada: {nome}")
            else:
                # Aqui você pode adicionar lógica para detectar ALTERAÇÕES em customizações existentes.
                # Isso é mais complexo e pode envolver comparar hashes de conteúdo ou datas de modificação.
                pass

    except pyodbc.Error as ex:
        # Captura erros de conexão ou consulta com o banco de dados.
        sqlstate = ex.args[0]
        print(f"Erro ao conectar ou consultar o banco de dados do ERP: {sqlstate}")
    finally:
        # O bloco 'finally' sempre é executado, com ou sem erro.
        if conn:
            conn.close() # Garante que a conexão com o banco de dados seja sempre fechada.

# Você pode agendar esta função para rodar periodicamente (ex: usando Celery ou um cron job)
# ou chamá-la via um endpoint de API para testes/gatilhos manuais.
