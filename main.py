# Compatibility patch for collections.abc.Sequence
import collections
if not hasattr(collections, 'Sequence'):
    import collections.abc
    collections.Sequence = collections.abc.Sequence

# Now import other necessary modules
import docx
import os
import sys
from PyPDF2 import PdfReader
import argparse
import ollama
import pandas as pd

def get_information_from_pdf(pdf_content, pdf_name):
    """
    Sends the PDF content to the LLaMA model and returns the extracted information.

    Args:
        pdf_content (str): The content extracted from the PDF.
        pdf_name (str): The name of the PDF file.

    Returns:
        dict: A dictionary containing extracted information like name, address, and price.
    """
    response = ollama.chat(
        model='llama3.1',
        messages=[{'role': 'user', 'content': 'Extract information from this document: ' + pdf_content}],
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
                        'address': {
                            'type': 'string',
                            'description': 'The address mentioned in the document',
                        },
                        'price': {
                            'type': 'string',
                            'description': 'The price or cost mentioned in the document',
                        }
                    },
                    'required': ['name', 'address', 'price'],
                },
            },
        }],
    )
    
    # Assuming the response is in a format that can be directly used
    # Adjust this according to how the response is actually structured
    extracted_info = {
        'pdf_name': pdf_name,
        'name': response.get('name', 'N/A'),
        'address': response.get('address', 'N/A'),
        'price': response.get('price', 'N/A')
    }
    
    return extracted_info

def extract_text_from_pdfs(directory, output_csv):
    """
    Extracts text from all PDF files in the specified directory and saves the extracted information to a CSV file.
    
    Args:
        directory (str): The path to the directory containing PDFs.
        output_csv (str): The path to the output CSV file.
    """
    pdf_files = find_pdf_files(directory)
    extracted_data = []

    for file in pdf_files:
        with open(file, 'rb') as f:
            pdf_reader = PdfReader(f)
            text = ''
            for page in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page].extract_text()

            extracted_info = get_information_from_pdf(text, os.path.basename(file))
            extracted_data.append(extracted_info)

    # Convert the extracted data to a DataFrame and save it to a CSV file
    df = pd.DataFrame(extracted_data)
    df.to_csv(output_csv, index=False)
    print(f"Extracted information has been saved to {output_csv}")

def find_pdf_files(directory):
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

def main():
    """
    The entry point of the script.
    
    Args:
        None
    
    Returns:
        None
    """
    parser = argparse.ArgumentParser(description='Extract text from PDFs and save to CSV')
    parser.add_argument('--directory', required=True, help='Directory containing PDF files')
    parser.add_argument('--output_csv', required=True, help='Path to the output CSV file')
    args = parser.parse_args()

    extract_text_from_pdfs(args.directory, args.output_csv)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: python main.py --help")
        sys.exit(1)
    
    main()