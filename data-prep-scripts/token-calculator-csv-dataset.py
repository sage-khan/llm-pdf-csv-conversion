import csv #Provides functionality to read from and write to CSV files.
import nltk #A popular natural language processing (NLP) library in Python. Here, it's used for tokenizing text.

# Download the Punkt tokenizer models for tokenization
nltk.download('punkt') #downloads the punkt tokenizer models, which are used by the nltk library to split text into tokens (words).

def count_tokens(text): #This function takes a string text and uses the nltk.word_tokenize method to split it into tokens. It then returns the count of these tokens.
    tokens = nltk.word_tokenize(text)
    return len(tokens)

def calculate_tokens(filename): #This function reads data from a CSV file and computes various statistics about the tokens in each row and column. 
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile) #It uses the csv.DictReader to read the CSV file into a dictionary format where each row is represented as a dictionary with column headers as keys.
        
        # Initialize dictionaries to store token counts and number of cells for each column. Within the calculate_tokens function, several dictionaries and lists are initialized to keep track of the counts
        token_counts = {'instruction': 0, 'input': 0, 'output': 0} #Stores the total count of tokens for each of the specified columns (instruction, input, output).
        num_cells = {'instruction': 0, 'input': 0, 'output': 0} #Counts the number of cells processed for each column.
        
        # Initialize list to store total tokens for each row
        row_tokens = [] #Keeps track of the total number of tokens per row.

      
        for row in reader: #Iterates over each row in the CSV file.
            row_token_count = 0
            
            for column in ['instruction', 'input', 'output']:
                cell_content = row[column].strip() if row[column] else "" #For each column of interest, it strips whitespace, checks if the cell is empty, and then counts the tokens using count_tokens.
                
                # Calculate tokens for the cell
                tokens = count_tokens(cell_content)
                
                # Update token count and number of cells # Updates token_counts and num_cells dictionaries with the new counts.
                token_counts[column] += tokens
                num_cells[column] += 1
                
                # Update row token count
                row_token_count += tokens
            
            # Store total tokens for the row #Adds the row's total token count to row_tokens.
            row_tokens.append(row_token_count)

      #Post-Processing - After all rows have been processed, the function calculates

        # Calculate total tokens for each column
        total_tokens_column = {column: token_counts[column] for column in ['instruction', 'input', 'output']}
        
        # Calculate average tokens per cell for each column #Average number of tokens per cell for each column, computed as the total tokens divided by the number of cells (if greater than zero).
        average_tokens_column = {column: token_counts[column] / num_cells[column] if num_cells[column] > 0 else 0
                                 for column in ['instruction', 'input', 'output']}
        
        # Calculate total tokens for each row #Sum of all tokens in all rows.
        total_tokens_row = sum(row_tokens)
        
        # Calculate general sum of all tokens #Total sum of all tokens across all columns.
        general_sum_tokens = sum(token_counts.values())
        
        # Calculate total tokens per column # Sum of all tokens per column, effectively a duplicate of general_sum_tokens for this context
        total_tokens_per_column = sum(total_tokens_column.values())
        
        return total_tokens_column, average_tokens_column, total_tokens_row, general_sum_tokens, total_tokens_per_column

 
if __name__ == '__main__': #If the script is run as the main module, it calls calculate_tokens with a specific filename, computes the token statistics, and then prints them.
    filename = 'final_output.csv'  # Replace with your CSV filename
    
    total_tokens_column, average_tokens_column, total_tokens_row, general_sum_tokens, total_tokens_per_column = calculate_tokens(filename)

#The script prints: Total and average tokens for each column, Total tokens per row, General sum of all tokens and total tokens per column.
    print("Total tokens, average tokens per cell, total tokens per row, general sum of all tokens, and total tokens per column:")
    
    # Print total tokens for each column
    print("\nTotal tokens for each column:")
    for column, total_tokens in total_tokens_column.items():
        print(f"{column}: {total_tokens}")
    
    # Print average tokens per cell for each column
    print("\nAverage tokens per cell for each column:")
    for column, avg_tokens in average_tokens_column.items():
        print(f"{column}: {avg_tokens:.2f}")
    
    # Print total tokens per row
    print(f"\nTotal tokens per row: {total_tokens_row}")
    
    # Print the general sum of all tokens
    print(f"\nGeneral sum of all tokens: {general_sum_tokens}")
    
    # Print total tokens per column
    print(f"\nTotal tokens per column: {total_tokens_per_column}")
