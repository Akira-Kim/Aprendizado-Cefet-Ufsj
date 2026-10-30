import PyPDF2
import re
import string

# Abre o arquivo PDF em modo de leitura binária
nome_arquivo_pdf = "artigoracismo.pdf"  # Substitua pelo nome do seu arquivo PDF
pdf_file = open(nome_arquivo_pdf, "rb")

# Cria um objeto PDFReader
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Inicializa uma string para armazenar o texto extraído
texto_extraido = ""

# Percorre todas as páginas do PDF e extrai o texto
for page in pdf_reader.pages:
    texto_extraido += page.extract_text()

# Fecha o arquivo PDF
pdf_file.close()

# Processamento do texto:
# 1. Remove números do texto inteiro ANTES de dividir em palavras
texto_sem_numeros = re.sub(r'\d+', '', texto_extraido)

# 2. Remove palavras com apenas 1 caractere (incluindo pontuações isoladas)
#    Usando expressão regular com \b (word boundaries)
texto_filtrado = re.sub(r'\b\w\b', '', texto_sem_numeros)

# 3. Remove pontuações restantes e caracteres especiais
#    Cria uma tabela de tradução para remover pontuações
translator = str.maketrans('', '', string.punctuation)
texto_limpo = texto_filtrado.translate(translator)

# 4. Divide o texto final em palavras
palavras = texto_limpo.split()

# Exibe as palavras filtradas
for palavra in palavras:
    # Filtra palavras vazias que possam ter sobrado
    if palavra:
        print(palavra)