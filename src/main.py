import os
import config
import utilitarios as utils
from processador import processar_arquivo

def main():
    
    utils.setup_inicial()
    
    print(f"\n--- SISTEMA DE ORGANIZAÇÃO DE DOCUMENTOS ---")
    print(f"Lendo arquivos de: {config.DIR_ENTRADA}")
    print(f"Logs salvos em: {config.DIR_LOGS}")
    print("--------------------------------------------\n")

   
    arquivos = [f for f in os.listdir(config.DIR_ENTRADA) if f.lower().endswith('.pdf')]

    if not arquivos:
        print("Nenhum arquivo PDF encontrado na pasta 'entrada'.")
        return

    
    for arquivo in arquivos:
        caminho_completo = os.path.join(config.DIR_ENTRADA, arquivo)
        processar_arquivo(caminho_completo)

    print("\n--- Processamento Concluído ---")

if __name__ == "__main__":
    main()