import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

pdf_path = 'saida.pdf'
extracted_text = extract_text_from_pdf(pdf_path)

output_txt_path = 'arquivo_extraido.txt'
with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
    txt_file.write(extracted_text)

print("Texto extraído e salvo em", output_txt_path)