import os
import sys
from PyPDF2 import PdfFileReader
from pdfplumber import pdf
import argparse

import ollama

def get_information_from_pdf(pdf_content):
    response = ollama.chat(
        model='llama3.1',
        messages=[{'role': 'user', 'content': 
            'Quels sont les informations dans ce document ? Nom, adresse, prix'}],

        # provide a push pdf
        tools=[{
        'type': 'function',
        'function': {
            'name': 'push_pdf_info',
            'description': 'push pdf information',
            'parameters': {
            'type': 'object',
            'properties': {
                'name': {
                'type': 'string',
                'description': 'The name of the bill',
                },
            },
            'required': ['name'],
            },
        },
        },
    ],
    )

def get_pdf_files(directory):
    """
    Returns a list of PDF files in the specified directory.
    
    Args:
        directory (str): The path to the directory containing PDFs.
    
    Returns:
        list: A list of PDF file names.
    """
    return [f for f in os.listdir(directory) if f.endswith('.pdf')]

def extract_text_from_pdfs(directory):
    """
    Extracts text from all PDF files in the specified directory.
    
    Args:
        directory (str): The path to the directory containing PDFs.
    """
    pdf_files = get_pdf_files(directory)
    for file in pdf_files:
        with open(os.path.join(directory, file), 'rb') as f:
            pdf_reader = PdfFileReader(f)
            text = ''
            for page in range(pdf_reader.numPages):
                text += pdf_reader.getPage(page).extractText()
            print(f"Extracted text from {file}:")
            print(text)

def main():
    """
    The entry point of the script.
    
    Args:
        None
    
    Returns:
        None
    """
    # Reverted change: Removed the --help check
    parser = argparse.ArgumentParser(description='Extract text from PDFs')
    parser.add_argument('--directory', required=True, help='Directory containing PDFs')
    args = parser.parse_args()

    extract_text_from_pdfs(args.directory)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: python main.py --help")
        sys.exit(1)
    
    main()
