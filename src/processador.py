import os
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader, PdfWriter
import config
import utilitarios as utils


pytesseract.pytesseract.tesseract_cmd = config.PATH_TESSERACT

def identificar_metadados(texto_pagina):
    
    texto_limpo = utils.limpar_texto(texto_pagina)
    
    func_encontrado = None
    cat_encontrada = None

   
    for nome_busca, pasta_destino in config.LISTA_FUNCIONARIOS.items():
        if nome_busca in texto_limpo:
            func_encontrado = pasta_destino
            break
    
    
    for categoria, palavras in config.CATEGORIAS.items():
        for palavra in palavras:
            if utils.limpar_texto(palavra) in texto_limpo:
                cat_encontrada = categoria
                break
        if cat_encontrada:
            break
            
    return func_encontrado, cat_encontrada

def salvar_buffer_pdf(writer, pasta_func, categoria, nome_base, contador):
    
    if len(writer.pages) == 0:
        return

   
    caminho_dir = os.path.join(config.DIR_SAIDA, pasta_func, categoria)
    if not os.path.exists(caminho_dir):
        os.makedirs(caminho_dir)

    nome_final = f"{nome_base}_PARTE_{contador}.pdf"
    caminho_arquivo = os.path.join(caminho_dir, nome_final)

    with open(caminho_arquivo, "wb") as f:
        writer.write(f)
    
    utils.registrar_log(f"Arquivo salvo: {pasta_func} -> {categoria} -> {nome_final}", "SUCESSO")

def processar_arquivo(caminho_arquivo_entrada):
    nome_arquivo = os.path.basename(caminho_arquivo_entrada)
    utils.registrar_log(f"Iniciando processamento de: {nome_arquivo}")

    try:
        
        leitor_pdf = PdfReader(caminho_arquivo_entrada)
        
       
        imagens = convert_from_path(caminho_arquivo_entrada, dpi=200, poppler_path=config.PATH_POPPLER)
        
        total_paginas = len(leitor_pdf.pages)
        
       
        func_atual = "DESCONHECIDOS"
        cat_atual = "GERAL"
        writer_atual = PdfWriter()
        contador_partes = 1
        paginas_no_buffer = 0

        for i in range(total_paginas):
            
            texto = pytesseract.image_to_string(imagens[i], lang='por')
            
            func_detectado, cat_detectada = identificar_metadados(texto)

           
            mudou_contexto = False
            
            if cat_detectada and cat_detectada != cat_atual:
                mudou_contexto = True
            
            if func_detectado and func_detectado != func_atual:
                mudou_contexto = True
               
                func_atual = func_detectado 

            if mudou_contexto and paginas_no_buffer > 0:
                utils.registrar_log(f"Mudança detectada na pág {i+1}. Salvando anterior...")
                salvar_buffer_pdf(writer_atual, func_atual, cat_atual, nome_arquivo, contador_partes)
                
                
                writer_atual = PdfWriter()
                paginas_no_buffer = 0
                contador_partes += 1
                
                
                if cat_detectada:
                    cat_atual = cat_detectada

           
            writer_atual.add_page(leitor_pdf.pages[i])
            paginas_no_buffer += 1

        
        if paginas_no_buffer > 0:
            salvar_buffer_pdf(writer_atual, func_atual, cat_atual, nome_arquivo, contador_partes)

    except Exception as e:
        utils.registrar_log(f"Erro fatal ao processar {nome_arquivo}: {e}", "ERRO")
        