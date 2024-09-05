
import pandas as pd
import gzip  # Import gzip for reading compressed files
import json


path_rating_cellPhones = './Cell_Phones_and_Accessories.csv.gz'
df_ratings_raw_cellPhones = pd.read_csv(path_rating_cellPhones)

# Select the first 20 rows
df_first_20 = df_ratings_raw_cellPhones.head(20)
print("Zain is here, trying to do some work.")
print("The only thing which matters is trying.")
print(df_first_20)

# Convert the selected rows to JSON format
json_data_first_20 = df_first_20.to_json(orient='records', lines=True)

# Save to a new JSON file
with open('small_cellPhones_csv.jsonl', 'w') as f:
    f.write(json_data_first_20)