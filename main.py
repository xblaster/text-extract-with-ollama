import argparse
import sys
from pdf_extractor import extract_text_from_pdfs

def main():
    """
    The entry point of the script.
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
