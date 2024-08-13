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
from PyPDF2 import PdfReader
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

def extract_text_from_pdfs(directory):
    """
    Extracts text from all PDF files in the specified directory.
    
    Args:
        directory (str): The path to the directory containing PDFs.
    """
    pdf_files = find_pdf_files(directory)
    for file in pdf_files:
        with open( file, 'rb') as f:
            pdf_reader = PdfReader(f)
            text = ''
            for page in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page].extract_text()
            print(f"Extracted text from {file}:")
            print(text)

def find_pdf_files(directory):
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    print(pdf_files)
    return pdf_files

def find_docx_files(directory):
    docx_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.docx'):
                docx_files.append(os.path.join(root, file))
    return docx_files


def extract_text_from_docx(directory):
    """
    Extracts text from all docx files in the specified directory.
    
    Args:
        directory (str): The path to the directory containing docx files.
    """
    docx_files = find_docx_files(directory)
    for file in docx_files:
        if file.endswith('.docx'):
            doc = docx.Document(os.path.join(directory, file))
            print(doc)
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
    # extract_text_from_docx(args.directory)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: python main.py --help")
        sys.exit(1)
    
    main()
