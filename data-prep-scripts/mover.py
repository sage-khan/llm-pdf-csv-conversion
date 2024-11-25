import os
import shutil

def move_files(src_folder, dest_folder):
    # Create "Last" directory if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for root, dirs, files in os.walk(src_folder):
        for file_name in files:
            if file_name.endswith('.pdf') or file_name.endswith('.csv'):
                src_path = os.path.join(root, file_name)
                dest_path = os.path.join(dest_folder, file_name)
                
                # Check if file with the same name exists in "Last" directory
                if not os.path.exists(dest_path):
                    shutil.move(src_path, dest_path)
                    print(f"Moved {file_name} to {dest_folder}")

if __name__ == "__main__":
    # Current directory where the script is executed
    current_directory = os.getcwd()
    
    # Destination folder named "Last"
    destination_folder = os.path.join(current_directory, "Last2")
    
    # Move PDFs and CSVs
    move_files(current_directory, destination_folder)
