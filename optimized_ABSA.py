import logging
import os
import json
import pandas as pd
from pyabsa import AspectTermExtraction as ATEPC, DeviceTypeOption
import nltk
from nltk.tokenize import sent_tokenize
from concurrent.futures import ThreadPoolExecutor, as_completed

nltk.download("punkt")

OUTPUT_REVIEWS_PATH = "./optimized_reviews_after_absa.json"

# Set up logging to a file
logging.basicConfig(
    filename="script_progress.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# Initialize the aspect extractor globally
def setup_aspect_extractor(language="english", use_cuda=False):
    device_option = DeviceTypeOption.CUDA if use_cuda else DeviceTypeOption.CPU
    return ATEPC.AspectExtractor(language, auto_device=device_option)


aspect_extractor = setup_aspect_extractor("english", use_cuda=True)


def generate_key(asin, reviewerID):
    return f"{asin}_{reviewerID}"


def save_json(data, file_path):
    """Save data to a JSON file."""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def process_reviews_chunk(reviews_chunk, batch_size=32):
    """Perform ABSA on each sentence of the reviews chunk."""
    filtered_reviews = []

    global aspect_extractor

    for idx, entry in reviews_chunk.iterrows():
        try:
            key = generate_key(entry["asin"], entry["user_id"])
            review_text = entry["text"]

            absa_results = aspect_extractor.predict(review_text, print_result=True)

            filtered_reviews.append(
                {
                    "text": review_text,
                    "aspect": absa_results.get("aspect"),
                    "sentiment": absa_results.get("sentiment"),
                    "asin": entry["asin"],
                    "user_id": entry["user_id"],
                }
            )
        except Exception as e:
            logging.error(
                f"Error processing review {entry['asin']} - {entry['user_id']}: {e}"
            )

    return filtered_reviews


def perform_absa_and_save(
    data, output_path, chunk_size=1000, batch_size=32, max_workers=10
):
    """Perform ABSA in parallel and save results."""
    filtered_reviews = []
    total_chunks = len(range(0, data.shape[0], chunk_size))
    print("Zain")
    # Log total number of chunks
    logging.info(f"Total chunks to process: {total_chunks}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_chunk = {
            executor.submit(
                process_reviews_chunk, data[i : i + chunk_size], batch_size
            ): i
            for i in range(0, data.shape[0], chunk_size)
        }

        for future in as_completed(future_to_chunk):
            try:
                print("Zain")
                print(future_to_chunk)
                result = future.result()
                filtered_reviews.extend(result)
                print(result)
                save_json(
                    filtered_reviews, output_path
                )  # Save intermediate results to reduce memory usage
                logging.info(
                    f"Processed chunk: {len(filtered_reviews)} reviews saved so far."
                )
            except Exception as exc:
                logging.error(f"Exception in processing chunk: {exc}")


import time  # Import the time module


def main():
    csv_path = "final_reviews_for_cellPhones_punctuated.csv"

    # Start timing
    start_time = time.time()

    reviews = pd.read_csv(csv_path)

    # Log script start
    logging.info("Script started")

    # Limit to first 100 reviews
    limited_reviews = reviews.head(100)

    # Perform ABSA and save results
    perform_absa_and_save(limited_reviews, OUTPUT_REVIEWS_PATH)

    # Log script completion
    logging.info("Script completed")

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    logging.info(f"Time taken for processing: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
