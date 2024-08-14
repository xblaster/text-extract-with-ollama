import os
from PyPDF2 import PdfReader
from llama_handler import get_information_from_pdf
from csv_handler import check_if_already_analyzed

def extract_text_from_pdfs(directory, output_csv, name= ""):
    """
    Recursively extracts text from all PDF files in the specified directory and its subdirectories,
    and saves the extracted information to a CSV file.
    
    Args:
        directory (str): The path to the directory containing PDFs.
        output_csv (str): The path to the output CSV file.
        name (str): The name to use in the LLaMA query.
    """
    pdf_files = find_pdf_files(directory)

    for file in pdf_files:
        if check_if_already_analyzed(file, output_csv):
            print(f"Skipping {file}, already analyzed.")
            continue
        
        with open(file, 'rb') as f:
            pdf_reader = PdfReader(f)
            text = ''
            for page in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page].extract_text()

            get_information_from_pdf(text, output_csv, name, file)
    
    # Recursively process subdirectories
    for root, dirs, files in os.walk(directory):
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            extract_text_from_pdfs(subdir_path, output_csv, name)

def find_pdf_files(directory):
    """
    Finds all PDF files in the given directory and returns a list of file paths.
    
    Args:
        directory (str): The path to the directory to search.
    
    Returns:
        list: A list of paths to PDF files.
    """
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return pdf_files
