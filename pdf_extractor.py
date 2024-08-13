import os
from PyPDF2 import PdfReader
from llama_handler import get_information_from_pdf

def extract_text_from_pdfs(directory, output_csv):
    """
    Extracts text from all PDF files in the specified directory and saves the extracted information to a CSV file.
    
    Args:
        directory (str): The path to the directory containing PDFs.
        output_csv (str): The path to the output CSV file.
    """
    pdf_files = find_pdf_files(directory)
    
    for file in pdf_files:
        with open(file, 'rb') as f:
            pdf_reader = PdfReader(f)
            text = ''
            for page in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page].extract_text()

            get_information_from_pdf(text, output_csv)

def find_pdf_files(directory):
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return pdf_files
