import ollama
from csv_handler import push_csv_info

def get_information_from_pdf(pdf_content, csv_file, max_retries=3):
    """
    Sends the PDF content to the LLaMA model and returns the extracted information.

    Args:
        pdf_content (str): The content extracted from the PDF.
        csv_file (str): The path to the output CSV file.
        max_retries (int): The maximum number of retries in case of errors.
    """
    retries = 0
    while retries < max_retries:
        try:
            response = ollama.chat(
                model='llama3.1',
                messages=[{'role': 'user', 'content': f'Extract information from this document and push it into csv file. The emitter is {name}. Think step by step to achieve the goal.\n\n### content ###\n:' + pdf_content}],
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
                print("The model didn't use the function. Its response was:")
                print(response['message']['content'])
                return
            
            for tool in response['message']['tool_calls']:
                if tool['function']['name'] == 'push_csv_info':
                    if "Pauline OLTMANNS" in  tool['function']['arguments']['name']:
                        raise Exception("can't be Pauline !")
                    push_csv_info(
                        tool['function']['arguments']['number'],
                        tool['function']['arguments']['name'],
                        tool['function']['arguments']['price'],
                        tool['function']['arguments']['date'],
                        csv_file
                    )
            break  # Exit loop if successful
        except Exception as e:
            retries += 1
            print(f"Error occurred: {e}. Retry {retries}/{max_retries}...")
            if retries == max_retries:
                print("Maximum retries reached. Unable to process the document.")