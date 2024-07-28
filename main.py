import ollama

def extract_info_from_pdf(pdf_content):
    # This is a placeholder for the actual implementation of extracting info from PDF
    return {
        'nom': 'John Doe',
        'date': '2022-01-01',
        'prix': 19.99,
    }

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
    
    print(response['message']['tool_calls'])
