
## Project Pipeline

This project processes Amazon reviews, applies sentiment analysis, and generates structured question-answer opinion pairs. The following steps outline the complete workflow:

### Step 1: Run `Main.py`

Load and process the dataset.

**Input:**

```python
load_dataset(
    "McAuley-Lab/Amazon-Reviews-2023",
    "raw_meta_Cell_Phones_and_Accessories",
    split="full",
    trust_remote_code=True,
)

df_review_raw_cellPhones = load_dataset(
    "McAuley-Lab/Amazon-Reviews-2023",
    "raw_review_Cell_Phones_and_Accessories",
    split="full",
    trust_remote_code=True,
)

df_ratings_raw_cellPhones = load_dataset(
    "McAuley-Lab/Amazon-Reviews-2023",
    "5core_rating_only_Cell_Phones_and_Accessories",
    split="full",
    trust_remote_code=True,
)



Here are all the steps combined in a single Markdown format for your README.md:

markdown
Copy code
## Project Pipeline

This project processes Amazon reviews, applies sentiment analysis, and generates structured question-answer opinion pairs. The following steps outline the complete workflow:

### Step 1: Run `Main.py`

Load and process the dataset.

**Input:**

```python
load_dataset(
    "McAuley-Lab/Amazon-Reviews-2023",
    "raw_meta_Cell_Phones_and_Accessories",
    split="full",
    trust_remote_code=True,
)

df_review_raw_cellPhones = load_dataset(
    "McAuley-Lab/Amazon-Reviews-2023",
    "raw_review_Cell_Phones_and_Accessories",
    split="full",
    trust_remote_code=True,
)

df_ratings_raw_cellPhones = load_dataset(
    "McAuley-Lab/Amazon-Reviews-2023",
    "5core_rating_only_Cell_Phones_and_Accessories",
    split="full",
    trust_remote_code=True,
)

Output:
metaData_for_cellPhones.pkl
reviews_wholeReview.txt
reviews_for_cellPhones_df_cleaned.csv
retrieved_items_dict.json


Step 2: Run puntuation_model.py
Punctuate the cleaned reviews.

Input:
reviews_for_cellPhones_df_cleaned.csv

Output:
final_reviews_for_cellPhones_punctuated.csv

Step 3: Run ABSA.py
Perform aspect-based sentiment analysis on the reviews.

Input:
final_reviews_for_cellPhones_punctuated.csv

Output:
final_reviews_after_absa.json

Step 4: Transform Data Schema Run transform_absa_for_rag.py
Convert final_reviews_after_absa.json into the required schema.

Input:
final_reviews_after_absa.json

Output:
transformed_data_for_100_blocks_neg.json
transformed_data_for_vector_database.json


Step 5: Run generating_qa_op_pairs.py
Generate negative question-answer opinion pairs.

Input:
metaData_for_cellPhones.pkl
wrong_aspects_3.pkl
transformed_data.json
retrieved_items_dict.json

Output:
100_blocks_neg.pkl


Step 6: Run pos_generating_op_pairs.py
Generate positive question-answer opinion pairs.

Input:
metaData_for_cellPhones.pkl
wrong_aspects_3.pkl
transformed_data.json
retrieved_items_dict.json

Output:
100_blocks_pos.pkl



#Installation
- python -m spacy download en_core_web_trf
- export NLTK_DATA=/home/stud/abedinz1/localDisk/opinionconv-refactor
- export IPYTHONDIR=/home/stud/abedinz1/localDisk/opinionconv-refactor/.ipython
- python -m nltk.downloader stopwords
- python MAIN.py
- python -W ignore MAIN.py
- pip3 install torch torchvision torchaudio
- When using bender if you want to update the python version
    a) Do module spider python
    b) module load python.xx
    c) if you have a shell file for job running, add module load python.xx in the shell file also



