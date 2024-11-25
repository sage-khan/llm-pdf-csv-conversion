import os
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError

# Set the base directory where the folders are located
base_dir = '/home/glitch/Desktop/NewFolder/dataset'  # Adjust this path as necessary

# Check if the base directory exists
if not os.path.exists(base_dir):
    print(f"The base directory {base_dir} does not exist.")
else:
    # Iterate through each folder in the base directory
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path):
            pdf_file = os.path.join(folder_path, f"{folder}.pdf")
            if os.path.isfile(pdf_file):
                print(f"Processing {pdf_file}...")
                try:
                    # Convert PDF to images
                    images = convert_from_path(pdf_file)
                    
                    # Save each image with the required name format
                    for i, image in enumerate(images, start=1):
                        image_file = os.path.join(folder_path, f"{folder}-{i}.jpg")
                        image.save(image_file, 'JPEG')
                        print(f"Saved {image_file}")
                except (PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError) as e:
                    print(f"Error processing {pdf_file}: {e}")
            else:
                print(f"No PDF file found in {folder_path}")
        else:
            print(f"{folder_path} is not a directory.")

    print("PDF conversion to images completed.")
