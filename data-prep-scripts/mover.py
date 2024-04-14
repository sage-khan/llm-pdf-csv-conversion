#Import Libraries 
import os #Provides a way of using operating system dependent functionality like reading or writing to the file system.
import shutil # Offers high-level operations on files and collections of files such as moving or copying files.

def move_files(src_folder, dest_folder): #Defines a function move_files that takes two parameters, src_folder (source directory) and dest_folder (destination directory).
    # Create "Last" directory if it doesn't exist
    if not os.path.exists(dest_folder):   #Before moving any files, the script checks if the destination folder exists. If it does not, os.makedirs() is used to create the directory.
        os.makedirs(dest_folder)
    
  #os.walk() is used to generate the file names in a directory tree by walking either top-down or bottom-up. 
  #For each directory in the tree rooted at directory src_folder (including src_folder itself), it yields a 3-tuple (dirpath, dirnames, filenames).
  
    for root, dirs, files in os.walk(src_folder):
        for file_name in files:  #This loop iterates over every file in files. The if statement filters files, processing only those that end with .pdf or .csv.
            if file_name.endswith('.pdf') or file_name.endswith('.csv'):   
                src_path = os.path.join(root, file_name)   #os.path.join() constructs the full path to the source file (src_path) and the intended path in the destination directory (dest_path).
                dest_path = os.path.join(dest_folder, file_name)
                
                # Check if file with the same name exists in "Last" directory
                if not os.path.exists(dest_path):   #Before moving a file, the script checks if a file with the same name already exists at the destination (dest_path). 
                    shutil.move(src_path, dest_path)
                    print(f"Moved {file_name} to {dest_folder}")  #If it does not exist, shutil.move() is used to move the file from src_path to dest_path. It then prints a confirmation message.

if __name__ == "__main__":   #This block ensures that the moving operation only executes when the script is run directly (not when imported as a module).
    # Current directory where the script is executed
    current_directory = os.getcwd()   #os.getcwd() gets the current working directory (where the script is executed).
    
    # The destination folder is set as a subdirectory "Last2" within the current directory.
    destination_folder = os.path.join(current_directory, "Last2")   
    
    # Finally, the move_files function is called with the current directory as the source and the newly defined "Last2" directory as the destination.
    move_files(current_directory, destination_folder)
