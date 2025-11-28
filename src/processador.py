import os
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader, PdfWriter
import config
import utilitarios as utils
import traceback


def _resolve_tesseract_path():
    caminho = config.PATH_TESSERACT
    # If the config value is a directory, check for tesseract.exe inside it
    if os.path.isdir(caminho):
        # search recursively for tesseract.exe inside the provided directory
        for root, dirs, files in os.walk(caminho):
            if 'tesseract.exe' in files:
                return os.path.join(root, 'tesseract.exe')
        candidatos = [os.path.join(caminho, 'tesseract.exe')]
    else:
        candidatos = [caminho, os.path.join(caminho, 'tesseract.exe')]

    # common install locations
    candidatos.extend([
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    ])

    for c in candidatos:
        if c and os.path.isfile(c):
            return c

    # fallback: try system PATH
    try:
        from shutil import which
        caminho_path = which('tesseract')
        if caminho_path:
            return caminho_path
    except Exception:
        pass

    return None


tess_exe = _resolve_tesseract_path()
if tess_exe:
    pytesseract.pytesseract.tesseract_cmd = tess_exe
else:
    # Log a clear error and raise so the caller can handle it
    import utilitarios as _utils
    _utils.registrar_log('Tesseract não encontrado. Defina PATH_TESSERACT em config.py com o caminho completo para o executável tesseract.exe', 'ERRO')
    raise FileNotFoundError('Tesseract executable not found; set PATH_TESSERACT to full path of tesseract.exe')

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
        utils.registrar_log(traceback.format_exc(), "ERRO")
        