import pandas as pd
from deepmultilingualpunctuation import PunctuationModel

# Load the CSV file containing the reviews
csv_input_path = './reviews_for_cellPhones_df_cleaned.csv'  # Path to your input CSV file
csv_output_path = './final_reviews_for_cellPhones_punctuated.csv'  # Path to save the output CSV file

# Load the CSV into a DataFrame
reviews_df = pd.read_csv(csv_input_path)

# Initialize the punctuation model
model = PunctuationModel()

# Ensure that the 'text' field exists
if 'text' in reviews_df.columns:
    # Process each review and punctuate the text
    for idx, row in reviews_df.iterrows():
        review_text = row['text']
        if pd.notna(review_text) and review_text.strip():  # Check if the review text is not empty
            try:
                # Restore punctuation for the review
                punctuated_text = model.restore_punctuation(review_text.strip())
                # Replace the original text with the punctuated version in the DataFrame
                reviews_df.at[idx, 'text'] = punctuated_text
            except Exception as e:
                print(f"Error processing review at index {idx}: {e}")
                # Optionally leave the original text if an error occurs
                reviews_df.at[idx, 'text'] = review_text
else:
    print("Error: 'text' column not found in the input CSV.")

# Save the updated DataFrame to a new CSV file
reviews_df.to_csv(csv_output_path, index=False)

print(f"Punctuated reviews have been saved to {csv_output_path}")
