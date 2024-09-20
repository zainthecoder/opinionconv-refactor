from deepmultilingualpunctuation import PunctuationModel

# Initialize the punctuation model
model = PunctuationModel()

# Define file paths
input_file_path = 'reviews_wholeReview.txt'  # Replace with your input file name
output_file_path = 'reviews_punct.txt' 

# Open the input and output files
with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
    # Process each line (review) from the input file
    for line in input_file:
        # Skip empty lines
        if line.strip():
            # Restore punctuation for the current line
            punctuated_line = model.restore_punctuation(line.strip())
            # Write the punctuated line to the output file with a newline character
            output_file.write(punctuated_line + '\n')

print(f"Punctuated reviews have been saved to {output_file_path}")
