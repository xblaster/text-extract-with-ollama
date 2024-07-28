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
            'What\'s in this doc? Name, address, price'}],

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
