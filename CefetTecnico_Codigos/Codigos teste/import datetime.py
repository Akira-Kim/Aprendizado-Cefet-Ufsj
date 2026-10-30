import PyPDF2
import re
import unidecode
from collections import Counter

# Função para remover acentos e pontuações de uma string
def remover_acentos_e_pontuacoes(texto):
    # Remove acentos usando a biblioteca unidecode
    texto_sem_acentos = unidecode.unidecode(texto)
    
    # Remove pontuações usando expressão regular
    texto_sem_pontuacoes = re.sub(r'[^\w\s]', '', texto_sem_acentos)
    
    return texto_sem_pontuacoes

# Abre o arquivo PDF em modo de leitura binária
nome_arquivo_pdf = "RPG.pdf"  # Substitua pelo nome do seu arquivo PDF
pdf_file = open(nome_arquivo_pdf, "rb")

# Cria um objeto PDFReader
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Inicializa uma string para armazenar o texto extraído
texto_extraido = ""

# Percorre todas as páginas do PDF e extrai o texto
for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    texto_extraido += page.extract_text()

# Fecha o arquivo PDF
pdf_file.close()

# Remove acentos e pontuações do texto extraído
texto_sem_acentos_e_pontuacoes = remover_acentos_e_pontuacoes(texto_extraido)

# Divide o texto em palavras
palavras = texto_sem_acentos_e_pontuacoes.split()

# Define padrões de regex para números e palavras com uma letra
padrao_numeros = re.compile(r'\b\d+\b')
padrao_uma_letra = re.compile(r'\b\w\b')
padrao_duas_letra = re.compile(r'\b\w\w\b')
padrao_tres_letra = re.compile(r'\b\w\w\w\b')

# Filtra e remove números e palavras com uma letra
palavras_filtradas = [palavra for palavra in palavras if not padrao_numeros.match(palavra) and not padrao_uma_letra.match(palavra) and not padrao_duas_letra.match(palavra) and not padrao_tres_letra.match(palavra)]

# Conta a frequência das palavras
contagem_palavras = Counter(palavras_filtradas)

# Selecione as 5 palavras mais comuns
palavras_comuns = contagem_palavras.most_common(10)

# Crie um título com as 5 palavras mais comuns
titulo = ' '.join(palavra for palavra, _ in palavras_comuns)

# Exiba o título
print("Título:", titulo)

