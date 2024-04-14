#Changes
#1. We no longer use a dictionary to store the file contents. Instead, we use a list data to store the content directly as rows.
#2. If a corresponding CSV file exists for a given text file, we directly read its content and append it to data.
#3. The data list is then converted to a DataFrame, and the DataFrame is saved directly to 'final_output.csv'.
#4. We've kept the original instructions and text content reading as it was.
#5. We handle the UnicodeDecodeError by attempting to read the CSV file using ISO-8859-1 encoding after failing to read with utf-8.

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






```
The provided Python script is a utility for processing pairs of `.txt` and `.csv` files located in a specified directory. It reads the content of each `.txt` file and its corresponding `.csv` file (if available), then organizes the contents along with a fixed instruction into a new CSV file. Here's a step-by-step explanation of what each part of the script does:

### Imports
```python
import os
import pandas as pd
import csv
```
- **`os`**: Used for interacting with the operating system, specifically for file and directory operations.
- **`pandas`**: A powerful data manipulation library that simplifies data analysis and manipulation tasks.
- **`csv`**: Provides functionality to handle CSV files. It's used here to specify the quoting method when saving the output DataFrame to a CSV.

### Function Definition: `process_files`
```python
def process_files(directory):
```
This function is designed to process files within a given `directory`.

### Initializing File Lists
```python
txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
```
- **`os.listdir(directory)`**: Retrieves a list of entries in the specified directory.
- The list comprehensions filter these entries to include only those ending with `.txt` and `.csv`, respectively.

### Initial Output
```python
print(f"Found {len(txt_files)} txt files: {txt_files}")
print(f"Found {len(csv_files)} csv files: {csv_files}")
```
These print statements provide an initial overview of the number of `.txt` and `.csv` files found, along with their names.

### Processing Files
```python
data = []
for txt_file in txt_files:
    ...
```
- Initializes a list called `data` to hold the content for later DataFrame creation.
- Iterates over each `.txt` file found.

### Fixed Instruction Content
```python
inst_content = "Extract account details and transaction details from this bank statement data and structure it into csv format. Make sure you dont leave out any details pertaining to account details and transaction details. Use only what is given in the data and donot make up any detail from your own. Also perform a reconciliation to check if data integrity is correct."
```
- This is a hardcoded instruction that will be included in every row of the output DataFrame.

### Reading `.txt` and `.csv` Files
```python
try:
    with open(txt_path, 'r', encoding='utf-8') as file:
        txt_content = file.read()
except UnicodeDecodeError:
    with open(txt_path, 'r', encoding='ISO-8859-1') as file:
        txt_content = file.read()
```
- Attempts to read the `.txt` file content using UTF-8 encoding; if a `UnicodeDecodeError` is encountered, it falls back to ISO-8859-1 encoding.

### Handling Corresponding `.csv` Files
```python
if csv_file in csv_files:
    try:
        ...
    except UnicodeDecodeError:
        ...
else:
    print(f"Warning: {csv_file} not found!")
    csv_content = "CSV file not found"
```
- Checks if a corresponding `.csv` file exists for each `.txt` file.
- If found, reads the `.csv` file content; handles potential encoding issues similarly.
- If not found, logs a warning and sets `csv_content` to a placeholder string.

### Data Aggregation
```python
data.append([inst_content, txt_content, csv_content])
```
- Appends a list containing the instruction, `.txt` content, and `.csv` content to the `data` list.

### Creating and Saving the DataFrame
```python
df = pd.DataFrame(data, columns=['instruction', 'input', 'output'])
df.to_csv(output_path, index=False, quoting=csv.QUOTE_NONNUMERIC)
```
- Creates a DataFrame from the `data` list with columns named 'instruction', 'input', and 'output'.
- Saves this DataFrame to a CSV file named `final_output.csv` in the specified directory, with non-numeric values quoted to handle commas and other special characters within text fields properly.

### Output Notification
```python
print(f"Output CSV created at: {output_path}")
```
- Informs the user that the output CSV file has been successfully created at the specified path.

### Example Usage
```python
directory = './'
process_files(directory)
```
This line sets the current directory as the working directory and calls the `process_files` function. 

Overall, the script is useful for extracting data from text and CSV files, combining it with instructions, and structuring it into a new CSV file in a standardized format. This might be particularly useful in scenarios where multiple data sources need to be merged and formatted consistently for further analysis or processing.


```
