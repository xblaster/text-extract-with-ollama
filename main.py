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

def push_csv_info(number, name, price, date, csv_file='output.csv'):
    """
    Pushes the provided information into a CSV file.

    Args:
        number (str): The name of the bill.
        name (str): The address mentioned in the document.
        price (str): The price or cost mentioned in the document.
        date (str): The date
        csv_file (str): The path to the CSV file. Default is 'output.csv'.
    """

    # Prepare the data as a dictionary
    data = {
        'number': number,
        'name': name,
        'price': price,
        'date': date
    }

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame([data])

    # Check if the CSV file exists
    if not os.path.isfile(csv_file):
        # If the file does not exist, write the DataFrame with headers
        df.to_csv(csv_file, index=False)
    else:
        # If the file exists, append the DataFrame without headers
        df.to_csv(csv_file, mode='a', header=False, index=False)

    print(f"Information pushed to {csv_file}" + str(data))

def get_information_from_pdf(pdf_content, csv_file):
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
        messages=[{'role': 'user', 'content': 'Extract information from this document and push it into csv file. The emitter is Pauline Oltmanns . Think step by step to achieve the goal\n\n ### content ### \n:' + pdf_content}],
        tools=[{
            'type': 'function',
            'function': {
                'name': 'push_csv_info',
                'description': 'push csv information',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'number': {
                            'type': 'string',
                            'description': 'The bill number. Example: 2024-08-01-01',
                        },
                        'name': {
                            'type': 'string',
                            'description': 'The name of the person who receive the bill. Usually before "A yutz". Can\'t be Pauline Oltmanns, she\'s the specialist emitter. Example : Martin Dupond',
                        },
                        'price': {
                            'type': 'string',
                            'description': 'The price or cost mentioned in the document. Example: 20€',
                        },
                        'date': {
                            'type': 'string',
                            'description': 'The date mentioned in the document: Exemple: 21/02/2021',
                        }
                    },
                    'required': ['number', 'name', 'price', 'date'],
                },
            },
        }],
    )

    # Check if the model decided to use the provided function
    if not response['message'].get('tool_calls'):
        print("The model didn't use the function. Its response was:")
        print(response['message']['content'])
        return
    
    # Process function calls made by the model
    if response['message'].get('tool_calls'):
        available_functions = {
        'push_csv_info': push_csv_info,
        }
        for tool in response['message']['tool_calls']:
            function_to_call = available_functions[tool['function']['name']]
            function_response = function_to_call(tool['function']['arguments']['number'], tool['function']['arguments']['name'], tool['function']['arguments']['price'], tool['function']['arguments']['date'], csv_file)


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

            extracted_info = get_information_from_pdf(text, output_csv)
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