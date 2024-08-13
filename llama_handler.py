import ollama
import time
import logging
from csv_handler import push_csv_info

logging.basicConfig(level=logging.INFO, filename='pdf_processor.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def validate_name(name):
    """
    Validates the name extracted from the document.
    
    Args:
        name (str): The name to validate.
    
    Raises:
        ValueError: If the name is forbidden.
    """
    forbidden_names = ["Pauline Oltmanns"]
    if any(forbidden_name in name for forbidden_name in forbidden_names):
        raise ValueError(f"Invalid name found: {name}")

def get_information_from_pdf(pdf_content, csv_file, name, max_retries=3):
    """
    Sends the PDF content to the LLaMA model and returns the extracted information with retries in case of errors.

    Args:
        pdf_content (str): The content extracted from the PDF.
        csv_file (str): The path to the output CSV file.
        name (str): The name to use in the LLaMA query.
        max_retries (int): The maximum number of retries in case of errors.
    """
    retries = 0
    backoff_time = 2  # initial backoff time in seconds
    while retries < max_retries:
        try:
            response = ollama.chat(
                model='llama3.1',
                messages=[{'role': 'user', 'content': f'Extract information from this document and push it into csv file. The emitter is "Pauline Oltmanns". Think step by step to achieve the goal.\n\n### content ###\n:' + pdf_content}],
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
                                    'description': 'The name of the person who receives the bill. Example: Martin Dupond',
                                },
                                'price': {
                                    'type': 'string',
                                    'description': 'The price or cost mentioned in the document. Example: 20€',
                                },
                                'date': {
                                    'type': 'string',
                                    'description': 'The date mentioned in the document. Example: 21/02/2021',
                                }
                            },
                            'required': ['number', 'name', 'price', 'date'],
                        },
                    },
                }],
            )

            if not response['message'].get('tool_calls'):
                logging.warning("The model didn't use the function. Its response was:")
                logging.warning(response['message']['content'])
                raise Exception("No tool used")

            for tool in response['message']['tool_calls']:
                arguments = tool['function']['arguments']

                validate_name(arguments.get('name', 'Unknown Name'))

                push_csv_info(
                    arguments.get('number', 'Unknown Number'),
                    arguments.get('name', 'Unknown Name'),
                    arguments.get('price', 'Unknown Price'),
                    arguments.get('date', 'Unknown Date'),
                    csv_file
                )
            break  # Exit loop if successful
        except Exception as e:
            retries += 1
            logging.error(f"Error occurred: {e}. Retry {retries}/{max_retries}...")
            if retries == max_retries:
                logging.critical("Maximum retries reached. Unable to process the document.")
            else:
                time.sleep(backoff_time)
                backoff_time *= 2  # Exponential backoff
