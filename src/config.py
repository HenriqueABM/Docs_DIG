import os


PATH_TESSERACT = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

PATH_POPPLER = None 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIR_ENTRADA = os.path.join(BASE_DIR, 'entrada')
DIR_SAIDA = os.path.join(BASE_DIR, 'saida_organizada')
DIR_LOGS = os.path.join(BASE_DIR, 'logs')
DIR_ERRO = os.path.join(BASE_DIR, 'erros_leitura')




LISTA_FUNCIONARIOS = {
    "JOAO SILVA": "Joao_Silva",
    "MARIA OLIVEIRA": "Maria_Oliveira",
    "CARLOS SANTOS": "Carlos_Santos"
}


CATEGORIAS = {
    "ADITIVOS E CONTRATOS": ["CONTRATO DE TRABALHO", "TERMO ADITIVO", "CLÁUSULA", "EMPREGADOR", "ADMISSAO"],
    "ASOS": ["ASO", "ATESTADO DE SAUDE", "MEDICO COORDENADOR", "APTO", "INAPTO", "EXAME CLINICO"],
    "AVISO E RECIBOS": ["AVISO PREVIO", "RECIBO DE PAGAMENTO", "HOLERITE", "LIQUIDO A RECEBER", "SALARIO"],
    "CERTIFICADOS": ["CERTIFICADO", "CONCLUSAO DE CURSO", "CARGA HORARIA", "TREINAMENTO", "CAPACITACAO"],
    "ALTERACOES FUNCIONAIS": ["ALTERACAO DE CARGO", "MUDANCA DE FUNCAO", "FICHA DE REGISTRO", "PROMOCAO"]
}