#This will rename PDF files and their corresponding CSV files in a specified directory. 
#Each file pair is given a standardized new name based on a sequential numbering system. 

#IMPORT LIBRARIES
import os #provides a portable way of using operating system-dependent functionality such as file and directory operations.

def rename_files(directory): #This function takes one argument, directory, which is the path to the directory containing the files to be renamed.
    # Get all files in the directory
  #os.listdir(directory): Lists all entries in the given directory.
  #os.path.isfile(os.path.join(directory, f)): Combines the directory and the file name into a full path and checks if this path refers to a file (as opposed to a directory or other types of entries).
  #The list comprehension filters the entries to include only files.
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Filters the previously obtained list of files to include only those whose names end with .pdf
    pdf_files = [f for f in files if f.endswith('.pdf')] #
    
    # Initializes a counter variable that will be used to generate the new file names.
    counter = 1


  #Iterates through each PDF file found in the directory.
  #Generates new file names using formatted strings. a{counter:07}.pdf creates a string that starts with a, followed by the counter value padded with zeros to ensure it is seven digits long, and ends with .pdf. 
  #A similar name is created for the corresponding CSV file.
    for pdf_file in pdf_files:
        # Create new file names
        new_pdf_name = f'a{counter:07}.pdf'
        new_csv_name = f'a{counter:07}.csv'
        
        # Rename PDF file
        os.rename(os.path.join(directory, pdf_file), os.path.join(directory, new_pdf_name)) #Uses os.rename() to rename the PDF file to the new name.
        
        # Rename corresponding CSV file if it exists
        csv_file = pdf_file.replace('.pdf', '.csv') #Constructs the name of a possible corresponding CSV file by replacing .pdf in the PDF file name with .csv.
        if csv_file in files:   #If this CSV file exists in the directory, it is also renamed to the new name specified.
            os.rename(os.path.join(directory, csv_file), os.path.join(directory, new_csv_name))
        
        # Increments the counter after each iteration to ensure that each file pair receives a unique set of sequential numbers.
        counter += 1

if __name__ == '__main__': #This code block ensures that the rename_files function is executed only if the script is run as the main module, not if imported.
    directory = '.'  # The directory is set to the current directory (.), which is where the script is being executed.
    rename_files(directory)


#This script is particularly useful in scenarios where standardized file naming is required for organizational or processing purposes. 
#It ensures that related PDF and CSV files maintain linked through consistent naming, which is helpful in automated data processing workflows.
