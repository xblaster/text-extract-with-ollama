# Compatibility patch for collections.abc.Sequence
import collections
if not hasattr(collections, 'Sequence'):
    import collections.abc
    collections.Sequence = collections.abc.Sequence

# Now import other necessary modules
import docx

# Your remaining code goes here

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

        # provide a push docx
        tools=[{
        'type': 'function',
        'function': {
            'name': 'push_docx_info',
            'description': 'push docx information',
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
        }],
    ),
    return response

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
            

def extract_text_from_docx(directory):
    """
    Extracts text from all docx files in the specified directory.
    
    Args:
        directory (str): The path to the directory containing docx files.
    """
    docx_files = [f for f in os.listdir(directory) if f.endswith('.docx')]
    for file in docx_files:
        doc = docx.Document(os.path.join(directory, file))
        text = ''
        for para in doc.paragraphs:
            text += para.text + '\n'
        print(f"Extracted text from {file}:")
        print(text)
        print(get_information_from_docx(text))

def main():
    """
    The entry point of the script.
    
    Args:
        None
    
    Returns:
        None
    """
    # Reverted change: Removed the --help check
    parser = argparse.ArgumentParser(description='Extract text from PDFs and docx')
    parser.add_argument('--directory', required=True, help='Directory containing PDFs and docx files')
    args = parser.parse_args()

    extract_text_from_pdfs(args.directory)
    extract_text_from_docx(args.directory)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: python main.py --help")
        sys.exit(1)
    
    main()
