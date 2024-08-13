import os
import argparse
from docx2pdf import convert
from commandr import command, Run

def convert_docx_to_pdf(docx_file):
    # Convert DOCX file to PDF
    convert(docx_file)

@command('convert')
def convert_directory(input_dir: str, dry_run: bool = False):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".docx"):
                docx_file = os.path.join(root, file)
                pdf_file = os.path.splitext(docx_file)[0] + '.pdf'
                
                if os.path.exists(pdf_file):
                    print(f"PDF already exists: {pdf_file}")
                elif dry_run:
                    print(f"Would convert: {docx_file} to {pdf_file}")
                else:
                    print(f"Converting: {docx_file} to {pdf_file}")
                    convert_docx_to_pdf(docx_file)

def main():
    parser = argparse.ArgumentParser(description="Convert all DOCX files in a directory (including subdirectories) to PDFs.")
    parser.add_argument("input_dir", type=str, help="Input directory to analyze (including subdirectories)")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode: output what would happen without doing the conversion")

    args = parser.parse_args()

    convert_directory(args.input_dir, args.dry_run)

if __name__ == "__main__":
    Run(main)
