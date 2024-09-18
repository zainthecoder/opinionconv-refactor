
import pandas as pd
import gzip  # Import gzip for reading compressed files
import json

# def parse(path):
#     data = []
#     with gzip.open(path, 'rt', encoding='utf-8') as f:
#         for l in f:
#             data.append(json.loads(l.strip()))
#         return(data)

def parse(path):
    data = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data

#Load Data

path_review_cellPhones = './small_cellPhones_reviews.jsonl'
data_review_raw_cellPhones = parse(path_review_cellPhones)
df_review_raw_cellPhones = pd.DataFrame.from_dict(data_review_raw_cellPhones)
print(df_review_raw_cellPhones.head(3))

#Data Cleaning
# Adding numnber of reviews
reviews_for_cellPhones = df_review_cellPhones.loc[df_review_cellPhones['asin'].isin(Cell_Phones_df.asin.unique())]
df_asin_numReviews = pd.DataFrame()
df_asin_numReviews['asin'] = reviews_for_cellPhones.groupby(by="asin").count()[['reviewText']].index
df_asin_numReviews['num_reviews'] = reviews_for_cellPhones.groupby(by="asin").count()[['reviewText']].reviewText.values

metaData_for_cellPhones = Cell_Phones_df.merge(df_asin_numReviews, on='asin', how='outer')
metaData_for_cellPhones.fillna(value=0, inplace=True)

metaData_for_cellPhones.head(3)

with open('./metaData_for_cellPhones.pkl', 'wb') as fp:
    pickle.dump(metaData_for_cellPhones, fp, protocol=4)
path_metaData_cellPhones = './meta_Cell_Phones_and_Accessories.json.gz'
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
