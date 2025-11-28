import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATH_TESSERACT = os.path.join(BASE_DIR, 'tessdata')


PATH_POPPLER = r'C:\Users\c00188\Documents\poppler-25.11.0\Library\bin'

DIR_ENTRADA = os.path.join(BASE_DIR, 'entrada')  # Pasta local
DIR_SAIDA = os.path.join(BASE_DIR, 'saida_organizada')
DIR_LOGS = os.path.join(BASE_DIR, 'logs')
DIR_ERRO = os.path.join(BASE_DIR, 'erros_leitura')

# --- REGRAS DE NEGÓCIO ---

LISTA_FUNCIONARIOS = {
    "JOAO SILVA": "Joao_Silva",
    "MARIA OLIVEIRA": "Maria_Oliveira",
    "CARLOS SANTOS": "Carlos_Santos"
}

CATEGORIAS = {
    "ADITIVOS E CONTRATOS": ["CONTRATO DE TRABALHO", "TERMO ADITIVO", "CLÁUSULA", "EMPREGADOR"],
    "ASOS": ["ASO", "ATESTADO DE SAUDE", "MEDICO COORDENADOR", "APTO", "INAPTO"],
    "AVISO E RECIBOS": ["AVISO PREVIO", "RECIBO DE PAGAMENTO", "HOLERITE", "LIQUIDO A RECEBER"],
    "CERTIFICADOS": ["CERTIFICADO", "CONCLUSAO DE CURSO", "CARGA HORARIA", "TREINAMENTO"],
    "ALTERACOES FUNCIONAIS": ["ALTERACAO DE CARGO", "MUDANCA DE FUNCAO", "FICHA DE REGISTRO"]
}