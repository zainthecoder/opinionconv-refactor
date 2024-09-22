from deepmultilingualpunctuation import PunctuationModel

# Initialize the punctuation model
model = PunctuationModel()

# Define file paths
input_file_path = 'reviews_wholeReview.txt'  # Input file with unpunctuated reviews
#output_file_path = 'reviews_punct.txt'       # Output file for punctuated reviews

# Open the input and output files
with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
    # Process each line (review) from the input file
    for line_number, line in enumerate(input_file, start=1):
        # Skip empty lines
        if line.strip():
            try:
                # Restore punctuation for the current line
                punctuated_line = model.restore_punctuation(line.strip())
                # Write the punctuated line to the output file with a newline character
                output_file.write(punctuated_line + '\n')
            except Exception as e:
                # Log the error and continue processing the next line
                print(f"Error processing review on line {line_number}: {e}")
                # Optionally write a placeholder or the original line to the output file in case of failure
                output_file.write(line.strip() + '\n')

print(f"Punctuated reviews have been saved to {output_file_path}")
