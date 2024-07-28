import ollama

<<<<<<< HEAD
def extract_info_from_pdf(pdf_content):
    # This is a placeholder for the actual implementation of extracting info from PDF
    return {
        'nom': 'John Doe',
        'date': '2022-01-01',
        'prix': 19.99,
    }
=======
import ollama
from create_excel_file import push_excel_file, create_excel_file

def get_information_from_pdf(pdf_content):
    # This function uses the LLaMA model to extract information from a PDF.
    response = ollama.chat(
        model='llama3.1',
        messages=[{'role': 'user', 'content': 
            'Quels sont les informations dans ce document ? Nom, adresse, prix'}],

            # provide a weather checking tool to the model
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
    Extracts text from all PDF files in the specified directory and uses LLaMA to get information.
    
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
            get_information_from_pdf(text)
>>>>>>> temp-branch

def main():
    pdf_content = open('example.pdf', 'r').read()
    extracted_info = extract_info_from_pdf(pdf_content)
    
    response = ollama.chat(
        model='llama3.1',
        messages=[{'role': 'user', 'content': 
            f"Nom: {extracted_info['nom']}, Date: {extracted_info['date']}, Prix: {extracted_info['prix']}"}],
        
    # provide a weather checking tool to the model
        tools=[{
          'type': 'function',
          'function': {
            'name': 'get_current_weather',
            'description': 'Get the current weather for a city',
            'parameters': {
              'type': 'object',
              'properties': {
                'city': {
                  'type': 'string',
                  'description': 'The name of the city',
                },
              },
              'required': ['city'],
            },
          },
        },
      ],
    )
    
<<<<<<< HEAD
    print(response['message']['tool_calls'])
=======
    Returns:
        None
    """
    # Reverted change: Removed the --help check
    parser = argparse.ArgumentParser(description='Extract text from PDFs')
    parser.add_argument('--directory', required=True, help='Directory containing PDFs')
    args = parser.parse_args()

    extract_text_from_pdfs(args.directory)
    
    push_excel_file()
    create_excel_file()
>>>>>>> temp-branch

if __name__ == '__main__':
    main()
