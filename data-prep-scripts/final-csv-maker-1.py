import os
import pandas as pd
import csv

def process_files(directory):
    # Initialize lists to hold file paths
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

    print(f"Found {len(txt_files)} txt files: {txt_files}")
    print(f"Found {len(csv_files)} csv files: {csv_files}")

    # Create a list to hold file contents
    data = []

    # Process each file
    for txt_file in txt_files:
        txt_path = os.path.join(directory, txt_file)
        
        # Derive corresponding csv file name from txt file
        csv_file = txt_file.replace('.txt', '.csv')
        csv_path = os.path.join(directory, csv_file)

        print(f"Processing: {txt_file}, {csv_file}")

        # Read Content from instruction
        inst_content = "Extract account details and transaction details from this bank statement data and structure it into csv format. Make sure you dont leave out any details pertaining to account details and transaction details. Use only what is given in the data and donot make up any detail from your own. Also perform a reconciliation to check if data integrity is correct."

        # Read content from txt file
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                txt_content = file.read()
        except UnicodeDecodeError:
            with open(txt_path, 'r', encoding='ISO-8859-1') as file:
                txt_content = file.read()

        # Check if corresponding csv file exists
        if csv_file in csv_files:
            try:
                with open(csv_path, 'r', encoding='utf-8') as file:
                    csv_content = file.read()
            except UnicodeDecodeError:
                with open(csv_path, 'r', encoding='ISO-8859-1') as file:
                    csv_content = file.read()
        else:
            print(f"Warning: {csv_file} not found!")
            csv_content = "CSV file not found"

        # Append contents to data list
        data.append([inst_content, txt_content, csv_content])

    # Create a DataFrame
    df = pd.DataFrame(data, columns=['instruction', 'input', 'output'])

    # Save the DataFrame to a new CSV file
    output_path = os.path.join(directory, 'final_output.csv')
    df.to_csv(output_path, index=False, quoting=csv.QUOTE_NONNUMERIC)

    print(f"Output CSV created at: {output_path}")


# Example usage
directory = './'
process_files(directory)
