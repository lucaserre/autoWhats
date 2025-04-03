import pandas as pd
import pywhatkit
import time
from datetime import datetime
import re

def formatar_numero_telefone(numero):
    """Formata o número de telefone para o formato do WhatsApp (+55)"""
    # Verifica se o número é um inteiro e converte para string
    if isinstance(numero, int) or isinstance(numero, float):
        numero = str(int(numero))
    
    # Se for None ou não for uma string válida após conversão
    if not numero or not isinstance(numero, str):
        return None
    
    # Remove caracteres não numéricos
    numero = re.sub(r'[^\d]', '', numero)
    
    # Verifica se o número tem o tamanho correto (com DDD)
    if len(numero) >= 10:  # Pelo menos DDD + número
        # Adiciona o código do país se não estiver presente
        if not numero.startswith('55'):
            numero = '55' + numero
        return '+' + numero
    return None

def carregar_dados_excel(caminho_arquivo):
    """Carrega os dados do arquivo Excel"""
    try:
        # Tenta ler o arquivo com diferentes encodings se necessário
        df = pd.read_excel(caminho_arquivo)
        
        # Verifica se as colunas esperadas existem
        colunas_necessarias = ['CONTRATO', 'CESSIONARIO', 'CONTATO', 'ABERTAS']
        colunas_encontradas = list(df.columns)
        
        # Print para debug
        print(f"Colunas no arquivo: {colunas_encontradas}")
        
        # Mapeia as colunas encontradas para os nomes esperados
        if len(colunas_encontradas) >= 4:
            colunas_padronizadas = {
                df.columns[0]: 'CONTRATO',
                df.columns[1]: 'CESSIONARIO',
                df.columns[2]: 'CONTATO',
                df.columns[3]: 'ABERTAS'
            }
            
            df = df.rename(columns=colunas_padronizadas)
        else:
            print("Arquivo não contém todas as colunas necessárias!")
            return None
        
        # Converte a coluna 'ABERTAS' para inteiro
        df['ABERTAS'] = pd.to_numeric(df['ABERTAS'], errors='coerce').fillna(0).astype(int)
        
        # Converte a coluna 'CONTATO' para string
        df['CONTATO'] = df['CONTATO'].astype(str)
        
        # Converte a coluna 'CONTRATO' para string
        df['CONTRATO'] = df['CONTRATO'].astype(str)
        
        return df
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return None

def enviar_mensagem_whatsapp(dataframe):
    """Envia mensagens WhatsApp para clientes inadimplentes"""
    mensagens_enviadas = 0
    falhas = 0
    
    # Log para registro das ações
    log_file = open("log_mensagens_whatsapp.txt", "w", encoding="utf-8")
    log_file.write(f"Início do envio de mensagens: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    log_file.write("-" * 80 + "\n")
    
    for index, row in dataframe.iterrows():
        try:
            contrato = str(row['CONTRATO'])
            nome = str(row['CESSIONARIO'])
            telefone = str(row['CONTATO'])
            parcelas = int(row['ABERTAS'])
            
            # Exibe informações para debug
            print(f"Processando: Contrato={contrato}, Nome={nome}, Telefone={telefone}, Parcelas={parcelas}")
            
            # Verifica se o telefone existe e é válido
            if pd.isna(telefone) or telefone == "" or telefone == "nan":
                log_file.write(f"FALHA - Contrato {contrato}: {nome} - Telefone não disponível\n")
                falhas += 1
                continue
            
            # Formata o número de telefone
            telefone_formatado = formatar_numero_telefone(telefone)
            if not telefone_formatado:
                log_file.write(f"FALHA - Contrato {contrato}: {nome} - Formato de telefone inválido: {telefone}\n")
                falhas += 1
                continue
            
            # Exibe o telefone formatado para debug
            print(f"Telefone formatado: {telefone_formatado}")
            
            # Obtém o primeiro nome
            primeiro_nome = nome.split()[0] if nome and nome != "nan" else "Cliente"
            
            # Personaliza a mensagem com base no número de parcelas
            if parcelas == 1:
                mensagem = f"Olá, {primeiro_nome}, identificamos que você possui {parcelas} parcela em aberto. Posso te enviar o PIX para realizar o acerto?"
            else:
                mensagem = f"Olá, {primeiro_nome}, identificamos que você possui {parcelas} parcelas em aberto. Posso te enviar o PIX para realizar o acerto?"
            
            # Obtém a hora atual para envio
            agora = datetime.now()
            hora = agora.hour
            minuto = agora.minute + 1  # Adiciona 1 minuto para dar tempo de processar
            
            # Ajusta a hora se o minuto for 60
            if minuto >= 60:
                hora += 1
                minuto -= 60
            
            # Envia a mensagem via WhatsApp
            pywhatkit.sendwhatmsg(telefone_formatado, mensagem, hora, minuto, wait_time=15, tab_close=True)
            
            # Espera um pouco entre os envios para evitar bloqueios
            time.sleep(20)
            
            # Registra sucesso no log
            log_file.write(f"SUCESSO - Contrato {contrato}: {nome} - Enviado para {telefone} - {parcelas} parcela(s) em aberto\n")
            mensagens_enviadas += 1
            
            # Exibe progresso
            print(f"Mensagem enviada ({mensagens_enviadas}/{len(dataframe)}): {nome}")
            
        except Exception as e:
            log_file.write(f"ERRO - Contrato {contrato if 'contrato' in locals() else 'N/A'}: {nome if 'nome' in locals() else 'N/A'} - {str(e)}\n")
            falhas += 1
            print(f"Erro ao enviar mensagem para {nome if 'nome' in locals() else 'cliente'}: {e}")
    
    # Finaliza o log
    log_file.write("-" * 80 + "\n")
    log_file.write(f"Fim do envio: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    log_file.write(f"Total de mensagens enviadas: {mensagens_enviadas}\n")
    log_file.write(f"Total de falhas: {falhas}\n")
    log_file.close()
    
    return mensagens_enviadas, falhas

def main():
    print("=" * 50)
    print("SISTEMA DE ENVIO DE MENSAGENS PARA INADIMPLENTES")
    print("=" * 50)
    
    # Usar o arquivo fixo
    caminho_arquivo = "msg.xlsx"
    print(f"Usando arquivo: {caminho_arquivo}")
    
    # Carrega os dados do arquivo
    df = carregar_dados_excel(caminho_arquivo)
    
    if df is not None:
        print(f"Arquivo carregado com sucesso. {len(df)} clientes encontrados.")
        
        # Exibe uma prévia dos dados
        print("\nPrévia dos dados:")
        print(df.head().to_string())
        
        # Confirmação antes de enviar
        confirmacao = input("\nDeseja prosseguir com o envio das mensagens? (S/N): ")
        
        if confirmacao.upper() == "S":
            enviados, falhas = enviar_mensagem_whatsapp(df)
            print(f"\nProcesso concluído. {enviados} mensagens enviadas, {falhas} falhas.")
            print("Confira o arquivo log_mensagens_whatsapp.txt para mais detalhes.")
        else:
            print("Operação cancelada pelo usuário.")
    else:
        print("Não foi possível carregar o arquivo. Verifique o caminho e formato.")

if __name__ == "__main__":
    main()