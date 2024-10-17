import random
import os
from transformers import pipeline

from pyabsa import AspectTermExtraction as ATEPC, DeviceTypeOption


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


def perform_absa_and_save(data, output_path, unique_ids):
    """Perform ABSA on each sentence of each review and save the results."""
    filtered_reviews = []
    for entry in data:
        print("#REVIE@")
        pprint.pprint(entry)
        key = generate_key(entry["asin"], entry["reviewerID"])
        if key in unique_ids:
            review_text = entry[
                "reviewText"
            ]  # Adjust the key based on your JSON structure
            sentences = sent_tokenize(review_text)
            for sentence in sentences:
                absa_result = aspect_extractor.predict(sentence, print_result=False)
                # print("@SENTENCE@")
                # pprint.pprint(absa_result)
                filtered_reviews.append(
                    {
                        "reviewText": sentence,
                        "aspect": absa_result.get("aspect"),
                        "sentiment": absa_result.get("sentiment"),
                        "asin": entry["asin"],
                        "reviewerID": entry["reviewerID"],
                    }
                )

    save_json(filtered_reviews, output_path)


def main():
    # reviews = load_json(REVIEWS_PATH)
    reviews = parse_gzip_json(REVIEWS_PATH)

    perform_absa_and_save(reviews, OUTPUT_REVIEWS_PATH, unique_ids)


if __name__ == "__main__":
    main()
