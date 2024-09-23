import random
import os
from transformers import pipeline
import pandas as pd
import pprint
from pyabsa import AspectTermExtraction as ATEPC, DeviceTypeOption
import nltk
from nltk.tokenize import sent_tokenize

# Ensure NLTK punkt is downloaded
nltk.download('punkt')

OUTPUT_REVIEWS_PATH = "./reviews_after_absa.json"

def setup_aspect_extractor(language="english"):
    """Initialize the Aspect Term Extraction model with the specified language."""
    return ATEPC.AspectExtractor(language, auto_device=DeviceTypeOption.AUTO)


# Initialize the aspect extractor
aspect_extractor = setup_aspect_extractor("english")


def generate_key(asin, reviewerID):
    """Generate a unique key from asin and reviewerID."""
    return f"{asin}_{reviewerID}"


def save_json(data, file_path):
    """Save data to a JSON file."""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def perform_absa_and_save(data, output_path):
    """Perform ABSA on each sentence of each review and save the results."""
    filtered_reviews = []
    for idx, entry in data.iterrows():
        try:
            key = generate_key(entry["asin"], entry["user_id"])

            review_text = entry[
                "text"
            ]  # Adjust the key based on your JSON structure
            sentences = sent_tokenize(review_text)
            for sentence in sentences:
                absa_result = aspect_extractor.predict(sentence, print_result=False)
                # print("@SENTENCE@")
                # pprint.pprint(absa_result)
                filtered_reviews.append(
                    {
                        "text": sentence,
                        "aspect": absa_result.get("aspect"),
                        "sentiment": absa_result.get("sentiment"),
                        "asin": entry["asin"],
                        "user_id": entry["user_id"],
                    }
                )
        except Exception as e:
            print("Exception: ",e)
            
    save_json(filtered_reviews, output_path)


def main():
    # Load the CSV file
    csv_path = "final_reviews_for_cellPhones_punctuated.csv"  # Path to your uploaded CSV
    reviews = pd.read_csv(csv_path)  # Load the CSV as a DataFrame
    #print("columns: ",reviews.head())
    #print(reviews)
    perform_absa_and_save(reviews, OUTPUT_REVIEWS_PATH)


if __name__ == "__main__":
    main()
