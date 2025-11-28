import os
import config
import utilitarios as utils
from processador import processar_arquivo

def iniciar_manual():
    # 1. Cria as pastas se não existirem
    utils.setup_inicial()
    
    print(f"\n==========================================")
    print(f"   SISTEMA DE ORGANIZAÇÃO (MODO MANUAL)   ")
    print(f"==========================================")
    print(f"Lendo arquivos da pasta: {config.DIR_ENTRADA}")
    print(f"Saída configurada para: {config.DIR_SAIDA}")
    print("------------------------------------------\n")

    # 2. Verifica quais arquivos estão na pasta entrada
    arquivos = [f for f in os.listdir(config.DIR_ENTRADA) if f.lower().endswith('.pdf')]

    if not arquivos:
        print("❌ Nenhum arquivo PDF encontrado na pasta 'entrada'.")
        print("Coloque o arquivo digitalizado lá e rode novamente.")
        return

    print(f"Encontrados {len(arquivos)} arquivos para processar.")

    # 3. Processa um por um
    for arquivo in arquivos:
        caminho_completo = os.path.join(config.DIR_ENTRADA, arquivo)
        
        print(f"\n>>> Processando: {arquivo}")
        try:
            processar_arquivo(caminho_completo)
            print(f"✅ Concluído: {arquivo}")
            
            # Opcional: Remover o arquivo da entrada após o sucesso para não processar de novo
            # os.remove(caminho_completo) 
            # print("   (Arquivo original removido da entrada)")
            
        except Exception as e:
            print(f"❌ Erro ao processar {arquivo}: {e}")

    print("\n==========================================")
    print("   TODOS OS PROCESSOS FINALIZADOS")
    print("==========================================")

if __name__ == "__main__":
    iniciar_manual()