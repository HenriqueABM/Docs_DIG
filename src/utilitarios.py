import os
import datetime
from unidecode import unidecode
from config import DIR_LOGS, DIR_SAIDA, DIR_ERRO, DIR_ENTRADA

def setup_inicial():
    
    pastas = [DIR_ENTRADA, DIR_SAIDA, DIR_LOGS, DIR_ERRO]
    for pasta in pastas:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"[SISTEMA] Pasta criada: {pasta}")

def limpar_texto(texto):
    
    if not texto:
        return ""
    return unidecode(texto).upper()

def registrar_log(mensagem, tipo="INFO"):
    
    data_hoje = datetime.datetime.now().strftime("%Y-%m-%d")
    hora_agora = datetime.datetime.now().strftime("%H:%M:%S")
    
    nome_arquivo_log = f"log_{data_hoje}.txt"
    caminho_log = os.path.join(DIR_LOGS, nome_arquivo_log)
    
    linha = f"[{hora_agora}] [{tipo}] {mensagem}\n"
    
    print(linha.strip())
    
    with open(caminho_log, "a", encoding="utf-8") as f:
        f.write(linha)