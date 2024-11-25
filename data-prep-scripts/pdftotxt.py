import os
import subprocess

def convert_pdf_to_text(pdf_file):
    # Generate txt filename by replacing '.pdf' with '.txt'
    txt_file = pdf_file.replace('.pdf', '.txt')
    
    # Use pdftotext command to convert pdf to txt with flags -layout and -nopgbrk
    command = ['pdftotext', '-layout', '-nopgbrk', pdf_file, txt_file]
    subprocess.run(command)

def scan_and_convert(root_dir):
    # Walk through the directory
    for dirpath, _, filenames in os.walk(root_dir):
        # Filter out only pdf files
        pdf_files = [f for f in filenames if f.endswith('.pdf')]
        
        # Convert each pdf file to txt
        for pdf_file in pdf_files:
            pdf_path = os.path.join(dirpath, pdf_file)
            convert_pdf_to_text(pdf_path)
            print(f"Converted {pdf_path} to {pdf_path.replace('.pdf', '.txt')}")

def main():
    # Get current directory
    current_dir = os.getcwd()

    # Scan and convert pdfs in the directory and subdirectories
    scan_and_convert(current_dir)

if __name__ == "__main__":
    main()
