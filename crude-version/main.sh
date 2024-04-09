#!/bin/bash

# Function to install necessary software, sync remote input directory, process files, move processed files, and clean up
setupEnvironment() {
    sudo apt-get install ocrmypdf poppler-utils rsync inotify-tools qpdf
}

setupVariables() {
    # Variables
    REMOTE_HOST="conversion@192.168.0.102"
    LOCAL_HOST="llm@192.168.0.80"
    REMOTE_INPUT_DIR="/srv/dev-disk-by-uuid-281ef326-2aff-405e-b1e4-061cebc27cad/VirtuousAccountants/Itax/File-to-be-converted"
    LOCAL_INPUT_DIR="$HOME/conversion-files"
    PROCESSED_DIR="$HOME/converted-source-files/$(date +%d-%m-%y)"
    REMOTE_PROCESSED_DIR="/srv/dev-disk-by-uuid-281ef326-2aff-405e-b1e4-061cebc27cad/VirtuousAccountants/Itax/Converted-Files"
    TEMPLATE_FILE="./template.txt"
}

rsync_remote2local() {
    # Sync remote input directory with local input directory
    rsync -avz --remove-source-files "$REMOTE_HOST":"$REMOTE_INPUT_DIR"/* "$LOCAL_INPUT_DIR"/
}


processAndMoveFiles() {
    # Process files
    for file in "$LOCAL_INPUT_DIR"/*; do
        if [[ -f "$file" ]]; then
            # Determine the output filename without its extension
            filename=$(basename -- "$file")
            extension="${filename##*.}"
            filename="${filename%.*}"

            if [[ "$extension" == "pdf" ]]; then
                # Process PDF files
                # Convert to searchable PDF
                ocrmypdf --force-ocr --optimize 1 "$file" "$LOCAL_INPUT_DIR"/"${filename}-ocr.${extension}"

                # Convert PDF to text
                pdftotext -layout -nopgbrk "$LOCAL_INPUT_DIR"/"${filename}-ocr.${extension}" "$LOCAL_INPUT_DIR"/"${filename}.txt"
            fi

            # Regardless of the file type, process the text to CSV
            echo "Processing ${filename}.txt to ${filename}.csv"
            python3 converter.py "$LOCAL_INPUT_DIR"/"${filename}.txt" "$TEMPLATE_FILE" "$LOCAL_INPUT_DIR"/"${filename}.csv"

            # The ollama command and awk command are commented out, but can be included as needed
            #ollama run mistral "You are a data formatting and structuring expert. You can format any data in json and csv format. Write down opening and closing balance, bank detail, account title along with all the transactions in $(cat ${filename}.txt)            
            #cat "${filename}.txt" | awk '{print $0","}' > "${filename}.csv"
        fi
    done

    # Move CSVs back to the remote processed directory
    echo "Sending csv from $LOCAL_INPU_DIR to $REMOTE_HOST":"$REMOTE_PROCESSED_DIR"
    rsync -avz "$LOCAL_INPUT_DIR"/*.csv "$REMOTE_HOST":"$REMOTE_PROCESSED_DIR"/
    echo "Sync from Local to Remote Completed"

    # Move processed source files to a dated folder
    mkdir -p "$PROCESSED_DIR"
    mv "$LOCAL_INPUT_DIR"/* "$PROCESSED_DIR"/ # Clear remote input directory (Be careful with this step to avoid accidental data loss)

    ##Clear remote directory if needed
    #ssh $REMOTE_HOST && rm -f "$REMOTE_INPUT_DIR"/*
}

## Call the setup environment function
echo "Setting up Environment"
setupEnvironment
echo "Environment Setup Completed"

#Call the Variables
echo "Setting up Variables"
setupVariables
echo "Variables Setup Completed"

#Synchronize
echo "Syncing"
rsync_remote2local
echo "Sync Completed"

# Call the function to process and move files
echo "Beginning conversion"
processAndMoveFiles
echo "Files Processed and moved to $PROCESSED_DIR"

# Optional: Clear remote input directory after processing
# Uncomment the line below to enable
# ssh "$REMOTE_HOST" && rm -f "$REMOTE_INPUT_DIR/*"


# Set the directory you want to watch
WATCH_DIR="$HOME/conversion-files"

# Function to watch a directory for new files and process them
watch_dir() {
    local WATCH_DIR="$1"  # The directory to watch

    echo "Watching directory: $WATCH_DIR for new files"
    inotifywait -m -e create -e moved_to "$WATCH_DIR" |
    while read -r directory events filename; do
        echo "New file detected: $filename"

        # Construct the full path of the new file
        local new_file="${directory}/${filename}"

        # Call the main processing script or function
        processAndMoveFiles "$new_file"
    done
}

## Call the watch_dir function with the directory you want to watch
#echo "Setting up Watch on $WATCH_DIR"
#watch_dir "$WATCH_DIR"


##Script Logic for UBUNTU. It should do following:
#1a. ssh into remote host conversion@192.168.0.110. Make sure you have certificates configured. (Need steps for that also) i.e. When prompted, you can press enter to save the key pair in the default location and with no passphrase for automation purposes (though for security, a passphrase is recommended for manual operations). "ssh-keygen -t rsa -b 4096" , ssh-copy-id conversion@192.168.0.110 i.e. This command will ask for the remote user's password. Once entered correctly, the local machine's public SSH key will be added to the ~/.ssh/authorized_keys file of the remote user, enabling passwordless SSH login.
  #1b. Check input folder /srv/dev-disk-by-uuid-281ef326-2aff-405e-b1e4-061cebc27cad/VirtuousAccountants/Itax/File-to-be-converted which is in remote host conversion@192.168.0.110 for any new document (pdf, txt, HTML, csv, image or whatever) and copy it locally in "~/conversion-files"
#1c. change directory to ~/conversion-files
#1d. script should have inotify enabled on ~/conversion-files to check if there is any new file input
#2a. run ocrmypdf linux commandline tool file and convert it into text searchable pdf named <filename>-ocr.<extension> i.e ocrmypdf --force-ocr --optimize 1 <filename>.pdf <filename>-ocr.<extension>
#2b. run pdftotext linux commandline tool on the <filename>-ocr.<extension> file and convert it into txt file with same name as original input file name (not the <filename>-ocr.<extension>)
#2c. run Linux command i.e ollama run mistral You are an expert in data formatting and structuring. Please read all contents of $(cat <filename>.txt) and structure it into csv style table format as per example given in $(cat ../template.txt)" >> <filename>.csv. the output of the above command is then saved as csv file in same folder which has same name as input doc file name e.g. if input doc name is a1.pdf then output csv name will be a1.csv. it will also save the output as text file i.e. a1.txt if input document is a1.pdf forexample.
#3. run #2a to #2c in a loop for all files within the local input folder i.e ~/conversion-files
#4. This csv will be copied /srv/dev-disk-by-uuid-281ef326-2aff-405e-b1e4-061cebc27cad/VirtuousAccountants/Itax/Converted-Files which is in conversion@192.168.0.110 remote host
#5a.Move all input files that were copied in local folder ~/conversion-files to ~/converted-source-files/<foldername is today's date as dd-mm-yy>
#5b The remote input folder is then cleared and then is continuously monitored for any other pdf file saved in the input folder.

