
import pandas as pd
import gzip  # Import gzip for reading compressed files
import json

def parse(path):
    data = []
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        for l in f:
            data.append(json.loads(l.strip()))
        return(data)


path_metaData_cellPhones = './meta_Cell_Phones_and_Accessories.jsonl.gz'
data_metaData_cellPhones = parse(path_metaData_cellPhones)
df_metaData_raw_cellPhones = pd.DataFrame.from_dict(data_metaData_cellPhones)
df_metaData_raw_cellPhones.head(2)

# Select the first 20 rows
df_first_20 = df_metaData_raw_cellPhones.head(20)

# Convert the selected rows to JSON format
json_data_first_20 = df_first_20.to_json(orient='records', lines=True)

# Save to a new JSON file
with open('small_cellPhones_meta.jsonl', 'w') as f:
    f.write(json_data_first_20)