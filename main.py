import ollama

def extract_info_from_pdf(pdf_content):
    # This is a placeholder for the actual implementation of extracting info from PDF
    return {
        'nom': 'John Doe',
        'date': '2022-01-01',
        'prix': 19.99,
    }

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
    
    print(response['message']['tool_calls'])

if __name__ == '__main__':
    main()
