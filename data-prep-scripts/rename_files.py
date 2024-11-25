import os

def rename_files(directory):
    # Get all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Filter PDF files
    pdf_files = [f for f in files if f.endswith('.pdf')]
    
    # Initialize counter
    counter = 1
    
    for pdf_file in pdf_files:
        # Create new file names
        new_pdf_name = f'a{counter:07}.pdf'
        new_csv_name = f'a{counter:07}.csv'
        
        # Rename PDF file
        os.rename(os.path.join(directory, pdf_file), os.path.join(directory, new_pdf_name))
        
        # Rename corresponding CSV file if it exists
        csv_file = pdf_file.replace('.pdf', '.csv')
        if csv_file in files:
            os.rename(os.path.join(directory, csv_file), os.path.join(directory, new_csv_name))
        
        # Increment counter
        counter += 1

if __name__ == '__main__':
    directory = '.'  # Current directory
    rename_files(directory)
