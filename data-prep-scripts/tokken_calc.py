import csv
import nltk

# Download the Punkt tokenizer models for tokenization
nltk.download('punkt')

def count_tokens(text):
    tokens = nltk.word_tokenize(text)
    return len(tokens)

def calculate_tokens(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Initialize dictionaries to store token counts and number of cells for each column
        token_counts = {'instruction': 0, 'input': 0, 'output': 0}
        num_cells = {'instruction': 0, 'input': 0, 'output': 0}
        
        # Initialize list to store total tokens for each row
        row_tokens = []
        
        for row in reader:
            row_token_count = 0
            
            for column in ['instruction', 'input', 'output']:
                cell_content = row[column].strip() if row[column] else ""
                
                # Calculate tokens for the cell
                tokens = count_tokens(cell_content)
                
                # Update token count and number of cells
                token_counts[column] += tokens
                num_cells[column] += 1
                
                # Update row token count
                row_token_count += tokens
            
            # Store total tokens for the row
            row_tokens.append(row_token_count)
        
        # Calculate total tokens for each column
        total_tokens_column = {column: token_counts[column] for column in ['instruction', 'input', 'output']}
        
        # Calculate average tokens per cell for each column
        average_tokens_column = {column: token_counts[column] / num_cells[column] if num_cells[column] > 0 else 0
                                 for column in ['instruction', 'input', 'output']}
        
        # Calculate total tokens for each row
        total_tokens_row = sum(row_tokens)
        
        # Calculate general sum of all tokens
        general_sum_tokens = sum(token_counts.values())
        
        # Calculate total tokens per column
        total_tokens_per_column = sum(total_tokens_column.values())
        
        return total_tokens_column, average_tokens_column, total_tokens_row, general_sum_tokens, total_tokens_per_column

if __name__ == '__main__':
    filename = 'final_output.csv'  # Replace with your CSV filename
    
    total_tokens_column, average_tokens_column, total_tokens_row, general_sum_tokens, total_tokens_per_column = calculate_tokens(filename)
    
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
    
    # Print general sum of all tokens
    print(f"\nGeneral sum of all tokens: {general_sum_tokens}")
    
    # Print total tokens per column
    print(f"\nTotal tokens per column: {total_tokens_per_column}")
