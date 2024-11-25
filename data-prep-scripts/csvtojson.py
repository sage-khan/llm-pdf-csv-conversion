import csv
import json
import sys

def csv_to_json(csv_file_path, json_file_path):
    # Set a larger field size limit
    maxInt = sys.maxsize
    decrement = True

    while decrement:
        decrement = False
        try:
            csv.field_size_limit(maxInt)
        except OverflowError:
            maxInt = int(maxInt/10)
            decrement = True

    # Open the CSV file
    with open(csv_file_path, mode='r') as csv_file:
        # Read the CSV file into a dictionary
        csv_reader = csv.DictReader(csv_file)
        
        # Create a list to hold all rows
        data = []
        
        # Iterate over each row in the CSV
        for row in csv_reader:
            # Add the row to the list
            data.append(row)
    
    # Write the data to a JSON file
    with open(json_file_path, mode='w') as json_file:
        # Write the data as JSON
        json.dump(data, json_file, indent=4)

# Example usage:
csv_file_path = './final_output.csv'  # Replace with your CSV file path
json_file_path = './final_output.json'  # Replace with desired JSON file path
csv_to_json(csv_file_path, json_file_path)
