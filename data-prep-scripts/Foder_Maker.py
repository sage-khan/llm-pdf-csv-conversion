import os
import shutil

# Get a list of all files in the current directory
files = [f for f in os.listdir() if os.path.isfile(f)]

# Get the unique prefixes (e.g., A00001, A00002, etc.)
prefixes = set(f.split('.')[0] for f in files)

# Loop through each unique prefix
for prefix in prefixes:
    # Create a directory for each prefix
    if not os.path.exists(prefix):
        os.makedirs(prefix)
    
    # Move files with the current prefix to the corresponding directory
    for f in files:
        if f.startswith(prefix):
            shutil.move(f, os.path.join(prefix, f))

print("Files have been organized into folders.")
