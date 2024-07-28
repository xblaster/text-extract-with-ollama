import os
from PyPDF2 import PdfFileReader
from pdfplumber import pdf

def get_pdf_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.pdf')]

def extract_text_from_pdfs(directory):
    pdf_files = get_pdf_files(directory)
    for file in pdf_files:
        with open(os.path.join(directory, file), 'rb') as f:
            pdf_reader = PdfFileReader(f)
            text = ''
            for page in range(pdf_reader.numPages):
                text += pdf_reader.getPage(page).extractText()
            print(f"Extracted text from {file}:")
            print(text)

if __name__ == '__main__':
    directory = '/path/to/your/directory'
    extract_text_from_pdfs(directory)
