#!/usr/bin/env python
# coding: utf-8

# # **IMPORT PACKAGES:**

import pandas as pd
import numpy as np
import gzip
import json
import os
import random
import re
import itertools
import glob
import string
from joblib import load
import pickle
import logging
import copy
import textstat

import matplotlib.pyplot as plt

import spacy
nlp_spacy = spacy.load("en_core_web_trf")

import nltk
#nltk.download('stopwords')
#nltk.download('punkt')

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

from IPython.display import Image
from IPython.core.display import HTML


# # **LOAD AMAZON DATASETS:**

### load the data
def parse(path):
    data = []
    with gzip.open(path) as f:
        for l in f:
            data.append(json.loads(l.strip()))
        return(data)



path_metaData_cellPhones = './meta_Cell_Phones_and_Accessories.json.gz'
data_metaData_cellPhones = parse(path_metaData_cellPhones)
df_metaData_raw_cellPhones = pd.DataFrame.from_dict(data_metaData_cellPhones)
df_metaData_raw_cellPhones.head(2)


# ### **2. Reviews**

path_review_cellPhones = './Cell_Phones_and_Accessories_5.json.gz'
data_review_raw_cellPhones = parse(path_review_cellPhones)
df_review_raw_cellPhones = pd.DataFrame.from_dict(data_review_raw_cellPhones)
df_review_raw_cellPhones.head(3)


# ### **3. Ratings**


cols = ["item", "user", "rating", "timestamp"]

path_rating_cellPhones = './Cell_Phones_and_Accessories.csv'
df_ratings_raw_cellPhones = pd.read_csv(path_rating_cellPhones, names = cols)

df_ratings_raw_cellPhones['timestamp'] = pd.to_datetime(df_ratings_raw_cellPhones['timestamp'],unit='s')


# # **DATA CLEANING:**


# Filter items with less than 6 categories & Split column of lists into multiple columns
df_metaData_raw_cellPhones_c1 = df_metaData_raw_cellPhones[df_metaData_raw_cellPhones.category.map(len) < 6 ]
df_categories_cellPhones = pd.DataFrame(df_metaData_raw_cellPhones_c1['category'].values.tolist()).add_prefix('category_')

df_metaData_concat_cellPhones = pd.concat([df_categories_cellPhones.reset_index(drop=True), df_metaData_raw_cellPhones_c1.reset_index(drop=True)], axis=1)

# Remove items without price
price_df_metaData_cellPhones = df_metaData_concat_cellPhones[df_metaData_concat_cellPhones.price != '']
# Remove items with wrong extracted price
price_df_metaData_cellPhones = price_df_metaData_cellPhones[price_df_metaData_cellPhones.price.str.len() < 9]
# Remove dollar ($) sign for sorting
price_df_metaData_cellPhones['price'] = price_df_metaData_cellPhones.price.str.replace('$', '').astype(float)

# Remove duplicates
subset = ['category_0', 'category_1', 'category_2', 'category_3', 'category_4', 'category', 'tech1', 'description', 'fit', 'title', 'also_buy', 'image',
       'tech2', 'brand', 'feature', 'rank', 'also_view', 'details', 'main_cat', 'date', 'price']

df_metaData_cellPhones = price_df_metaData_cellPhones.loc[price_df_metaData_cellPhones.astype(str).drop_duplicates(subset=subset, keep='first', inplace=False).index]
df_metaData_cellPhones.head(2)


# Add rating
df_ratings_cellPhones = df_ratings_raw_cellPhones.groupby(by="item").agg(num_ratings=('rating', 'count'), sum_ratings=('rating', 'sum'))
df_ratings_cellPhones['avg_rating'] = df_ratings_cellPhones.sum_ratings / df_ratings_cellPhones.num_ratings
df_ratings_cellPhones['asin'] = df_ratings_cellPhones.index
df_ratings_cellPhones.head(3)


# Merge df_metaData and df_ratings
df_metaData_ratings_cellPhones = pd.merge(df_metaData_cellPhones, df_ratings_cellPhones, on='asin')
df_metaData_ratings_cellPhones.head(2)


# Filter the items which have "Cell Phones" in category_1 and the main_category == "Cell Phones & Accessories"
Cell_Phones_df_raw = df_metaData_ratings_cellPhones[df_metaData_ratings_cellPhones.category_1 == 'Cell Phones']
Cell_Phones_df_raw = Cell_Phones_df_raw[Cell_Phones_df_raw.main_cat == "Cell Phones & Accessories"]

# Useful Cols
subset_cols = ['category_0', 'category_1', 'category_2', 'category_3', 'category_4', 'description', 'title', 'also_buy', 'image',
 'brand', 'feature', 'rank', 'also_view', 'details', 'main_cat', 'similar_item', 'date', 'price', 'num_ratings', 'avg_rating', 'asin']

Cell_Phones_df_raw = Cell_Phones_df_raw[subset_cols]
Cell_Phones_df_raw.reset_index(drop=True, inplace=True)

# Merging 3 columns: description, feature & title
all_features = Cell_Phones_df_raw[['description', 'feature', 'title']].values.tolist()
col_all_features = []
for i in all_features:
    list_features = []
    for j in i:
        if j:
            if type(j) == list:
                for k in j:
                    list_features.append(k)
            else:
                list_features.append(j)
    col_all_features.append(' ****** '.join(list_features))
    
Cell_Phones_df_raw["all_features"] = col_all_features
Cell_Phones_df_raw.head(2)


# Remove some useless brands
remove_brand_list = [Cell_Phones_df_raw[Cell_Phones_df_raw.brand == 'OtterBox'],
                     Cell_Phones_df_raw[Cell_Phones_df_raw.brand == 'Saunders'],
                     Cell_Phones_df_raw[Cell_Phones_df_raw.brand == 'F FORITO']]

remove_indices = []
remove_asin = []
for i in remove_brand_list:
    remove_df = i
    remove_indices.append(list(remove_df.index.values))
    remove_asin.append(list(remove_df.asin.values))
    
remove_indices = np.array(remove_indices).flatten()
remove_asin = np.array(remove_asin).flatten()

Cell_Phones_df_raw.drop(remove_indices, axis=0, inplace=True)


# Replace wrong brands
replace_brand_lists = [[['Unknown'], ['BlackBerry', 'Alcatel', 'LG', 'LG']],
                      [['AT&T'], ['ZTE', 'Huawei', 'ZTE', 'ZTE', 'ZTE', 'ZTE']],
                      [['Nexus'], ['Motorola', 'Google']],
                      [['Tracfone'], ['Motorola', 'Alcatel', 'LG', 'Alcatel', 'ZTE', 'LG', 'LG', 'Motorola']],
                      [['FreedomPop'], ['Samsung', 'Samsung', 'Samsung', 'Motorola']],
                      [[''], ['Alcatel', 'BLU', 'Samsung', 'Motorola', 'LG', 'LG', 'Kyocera', 'LG', 'Alcatel',
                              'T-Mobile', 'Sony', 'LG', 'Letv', 'Yotaphone' , 'T-Mobile', 'Pantech', 'LG', 'Google']],
                      [['Blackberry'], ['BlackBerry']],
                      [['Net10'], ['ZTE', 'Huawei']],
                      [['Sanyo 8400'], ['Sanyo']],
                      [['Nextel'], ['Motorola']],
                      [['Sprint'], ['Sanyo']],
                      [['LGIC'], ['LG']],
                      [['Verizon'], ['Samsung']],
                      [['DCP Products'], ['Pantech']],
                      [['Caterpillar'], ['Cat']],
                      [['Tellme'], ['Emporia']],
                      [['Boost Mobile'], ['Kyocera']],
                      [['P710'], ['LG']],
                      [['ZTE USA'], ['ZTE']],
                      [['NET10'], ['LG']],
                      [['T Mobile'], ['Alcatel']],
                      [['MOTCB'], ['Motorola']],
                      [['TRACFONE WIRELESS, INC.'], ['LG']],
                      [['Samsung Korea'], ['Samsung']],
                      [['Quality One Wireless'], ['Alcatel']],
                      [['Porsche Design'], ['BlackBerry']],
                      [['Moto X'], ['Motorola']],
                      [['Thailand'], ['THL']],
                      [['INEW'], ['Samsung']],
                      [['OneTouch'], ['Alcatel']],
                      [['VOWSVOWS'], ['BLU']],
                      [['ASUS'], ['Asus']],
                      [['Galaxy S5'], ['Samsung']],
                      [['Samsung/Straight Talk'], ['Samsung']],
                      [['SoonerSoft Electronics'], ['LG']],
                      [['CAT PHONES'], ['Cat']],
                      [['Samsung Group'], ['Samsung']],
                      [['Peirui'], ['OnePlus']],
                      [['CT-Miami LLC'], ['BLU']],
                      [['iGearPro'], ['Samsung']],
                      [['Pixi'], ['Alcatel']],
                      [['Risio'], ['LG']]]

def replace_wrong_brands(replace_brand_lists, df):
    df = df.copy()
    for replace_brand_list in replace_brand_lists:
        wrong_brand = replace_brand_list[0][0]
        correct_brands = replace_brand_list[1]
        incorrect_df = df[df.brand == wrong_brand]   
        if len(correct_brands) > 1:
            incorrect_df_asin = incorrect_df.asin.values
            for i in range(len(incorrect_df_asin)):
                asin_ = incorrect_df_asin[i]
                brand_ = correct_brands[i]
                index = df.query('asin == @asin_').index.values[0]
                df.loc[index, 'brand'] = brand_

        elif len(correct_brands) == 1:
            brand_ = correct_brands[0]
            indices = incorrect_df.index.values
            for index in indices:
                df.loc[index, 'brand'] = brand_
    return(df)

Cell_Phones_df = replace_wrong_brands(replace_brand_lists=replace_brand_lists, df=Cell_Phones_df_raw)


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


def cleaning_process(text):
    cleaned_text = text.replace("\n\n", " ")
    cleaned_text = cleaned_text.replace("\n", " ")
    cleaned_text = cleaned_text.replace("#", " ")
    cleaned_text = cleaned_text.replace("*", " ")
    cleaned_text = cleaned_text.replace("+", " ")
    cleaned_text = cleaned_text.replace("\'", "'")
    cleaned_text = cleaned_text.replace(",,", " ")
    cleaned_text = cleaned_text.replace("--", " ")
    
    cleaned_text = re.sub(r"blogs.blackberry.com\S+", " ", cleaned_text)
    cleaned_text = re.sub(r"helpblog.blackberry.com\S+", " ", cleaned_text)
    
    # Remove repeated letters
    cleaned_text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(cleaned_text))
    
    clean_tags = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleaned_text = re.sub(clean_tags, " ", cleaned_text)

    clean_urls =re.compile(r'https?://\S+')
    cleaned_text = re.sub(clean_urls, " ", cleaned_text)
    cleaned_text = cleaned_text.replace("=", " ")
    cleaned_text = re.sub(' +', ' ', cleaned_text)
    cleaned_text = cleaned_text.strip()
    return(cleaned_text)


#@Vahid: Could we use the columns:Summary and Voting, somehow?
reviews_for_cellPhones_df = df_review_raw_cellPhones.loc[df_review_raw_cellPhones['asin'].isin(Cell_Phones_df.asin.unique())]
reviews_for_cellPhones_df = reviews_for_cellPhones_df.dropna(axis=0, subset=['reviewText'])

# Clean reviews and create a text file for all reviews
cellPhone_reviews = reviews_for_cellPhones_df.reviewText
cellPhone_reviews_cleaned = cellPhone_reviews.apply(cleaning_process)

reviews_for_cellPhones_df_cleaned = reviews_for_cellPhones_df.copy()
reviews_for_cellPhones_df_cleaned['reviewText'] = cellPhone_reviews_cleaned.values

wholeReview_reviews_for_cellPhones_df = pd.DataFrame()
wholeReview_reviews_for_cellPhones_df['Index'] = reviews_for_cellPhones_df_cleaned[['asin', 'reviewerID']].apply(lambda x: '_'.join(x), axis=1)
wholeReview_reviews_for_cellPhones_df['reviewText'] = reviews_for_cellPhones_df_cleaned.reviewText.values
wholeReview_reviews_for_cellPhones_df = wholeReview_reviews_for_cellPhones_df.dropna(axis=0, subset=['reviewText'])

reviews_for_cellPhones_df_cleaned.to_csv("./reviews_for_cellPhones_df_cleaned.csv")

with open(".../Data/GeneratedData/reviews_wholeReview.txt", "w") as f:
    for review in cellPhone_reviews_cleaned.values:
        _ = f.write(review + '\n')


# # **GENERATING PREFERENCES:**


brand_list = list(Cell_Phones_df.brand.unique())
os_list = ['ios', 'android', 'windows', 'No']
memory_list = ['2 GB', '4 GB', '8 GB', '16 GB', '32 GB', '64 GB', '128 GB', '256 GB', 'No']
color_list = ['White', 'Silver', 'Black', 'Red', 'Gold', 'No']

# Generate all possible combinations for the preferences
all_c = list(itertools.product(brand_list, os_list, memory_list, color_list))
all_combinations = []
for i in all_c:
    if i[1] == "ios":
        if i[1] == "apple":
            all_combinations.append(list(i))
    else:
        if i[1] != "apple":
            all_combinations.append(list(i))
            
all_combinations_dict = {}
for i, j in enumerate(all_combinations):
    all_combinations_dict[str(i+1)] = {}
    all_combinations_dict[str(i+1)]["brand"] = j[0]
    all_combinations_dict[str(i+1)]["os"] = j[1]
    all_combinations_dict[str(i+1)]["color"] = j[3]
    all_combinations_dict[str(i+1)]["memory"] = j[2]

for k,v in list(all_combinations_dict.items())[63:70]:
    print(k,v)
    
len(all_combinations_dict.keys())


# Generate conversations for the preferences
conversation_dict_part_1 = {}
for k1,v1 in list(all_combinations_dict.items()):
    conversation_dict_part_1["Conv_#" + str(k1)] = {}
    Agent_1 = "Hello, May I help you?"
    User_1 = "Hi, I would like to buy a Cell Phone"
    conversation_dict_part_1[f"Conv_#" + str(k1)]['Agent_1'] = Agent_1
    conversation_dict_part_1["Conv_#" + str(k1)]['User_1'] = User_1
    counter = 1
    for k2, v2 in list(v1.items()):
        counter += 1
        Agent = f"Any preference on {k2}?"
        User = v2
        conversation_dict_part_1["Conv_#" + str(k1)][f'Agent_{counter}'] = Agent
        conversation_dict_part_1["Conv_#" + str(k1)][f'User_{counter}'] = User


for k,v in list(conversation_dict_part_1.items())[50:55]:
    print(k,v)


def findWholeWord(w):
    return (re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search)

def rules_generator(preferences_dict, features):
    rules = []
    for k2, v2 in list(preferences_dict.items()):
        if k2 != "brand" and v2 != "No":
            rules.append(findWholeWord(str(v2))(features.lower()))
    return(rules)


# Retrieve items for the preferences
DF = Cell_Phones_df 
retrieved_items_dict = {}
for k1, v1 in list(all_combinations_dict.items()):
    list_retrieved_items_final = []
    rules = []
    brand_value = v1['brand']
    if brand_value == "No":
        df_retrieved_items_brand = DF
    else:
        df_retrieved_items_brand = DF[DF.brand == brand_value]
    zipped = list(zip(df_retrieved_items_brand.asin.values, df_retrieved_items_brand.all_features.values))
    list_retrieved_items_final = []
    for index, features in zipped:
        if features:
            rules = rules_generator(v1, features)
            if all(rules):
                list_retrieved_items_final.append(index)

    retrieved_items_dict[k1] = {}
    retrieved_items_dict[k1]['preferences'] = v1
    retrieved_items_dict[k1]['retrieved items'] = list_retrieved_items_final
    
with open('./retrieved_items_dict.json', 'w') as f:
    json.dump(retrieved_items_dict, f)


for k, v in list(retrieved_items_dict.items())[55:65]:
    print(k,v)


# # **PUNCTUATION:**

# **Punctuation Restoration using Transformer Models:** [GitHub](https://github.com/xashru/punctuation-restoration)  [Paper](http://noisy-text.github.io/2020/pdf/2020.d200-1.18.pdf)

# **1. Go to this folder: punctuation-restoration**
# 
# ```cd ./punctuation-restoration```
# 
# **2. Run the inference.py to create the file test_en_out.txt:**
# 
# ```python3 src/inference.py --pretrained-model=roberta-large --weight-path=roberta-large-en.pt --language=en --in-file=data/test_en.txt --out-file=data/test_en_out.txt``` 
# 
# **3. Copy the file test_en_out.txt to the spacy_tokenization folder and rename it:**
# 
# ```cp ./punctuation-restoration/data/test_en_out.txt ./spacy_tokenization/data/input/reviews_punct.txt``` 


with open('./reviews_punct.txt') as f:
    lines = f.readlines()

lines[100]


# # **SENTENCE TOKENIZATION:**

# **1. Go to this folder: spacy_tokenization**
# 
# ```cd ./spacy_tokenization```
# 
# **2. Run the spacy_tokenization_punct.py:**
# 
# ```python3 spacy_tokenization_punct.py```


with open('./cellPhone_data_punct.json') as json_file:
    cellPhone_data_punct = json.load(json_file)
for i,j in list(cellPhone_data_punct.items())[:2]:
    print(i, j)


punct_reviews_for_cellPhones = pd.read_csv('./punct_reviews_for_cellPhones.csv')
punct_reviews_for_cellPhones.head(3)
punct_reviews_for_cellPhones.shape


cellPhone_data_punct_json = pd.read_json('./cellPhone_data_punct.json')
cellPhone_data_punct_json = cellPhone_data_punct_json.T
cellPhone_data_punct_json

num_tokens = []
for i in cellPhone_data_punct_json.label.values:
    num_tokens.append(len(i))
print("NUMBER OF REVIEWS:", len(num_tokens))

import matplotlib.pyplot as plt
ax = plt.axes()
ax.set_yscale('log')
_ = plt.hist(num_tokens, bins='auto')

print("AVERAGE OF NUM_TOKENS:", np.mean(np.array(num_tokens)))

max_length = 0
for i in cellPhone_data_punct_json.label.values:
    new_length = len(i)
    if new_length > max_length:
        max_length = new_length
print("MAX_LENGTH:", max_length)


# # **ASPECT EXTRACTION:**

# **Improving BERT Performance for Aspect-based Sentiment Analysis:** [GitHub](https://github.com/IMPLabUniPr/BERT-for-ABSA/tree/H-SUM)  [Paper](https://arxiv.org/pdf/2010.11731.pdf)

# **1. Go to this folder: BERT-for-ABSA**
# 
# ```cd ./BERT-for-ABSA```
# 
# **2. Copy the file: cellPhone_data_punct.json from spacy tokenization folder to BERT-for-ABSA:**
# 
# ```cp ./cellPhone_data_punct.json ./BERT-for-ABSA/ae/laptop/test.json```
# 
# **3. Run the aspect extraction script:**
# 
# ```bash script/run_absa.sh ae laptop_pt laptop pt_ae 9 0```


def IOB_to_tokens(tags, tokens):
    aspects = []
    for idx , tag in enumerate(tags):
        if tag == "B":
            idx_B_start = idx + 1
            token_B_start = tokens[idx]
            for idx_ , tag_ in enumerate(tags[idx_B_start:]):
                if tag_ == "I":
                    idx_next = idx_B_start + idx_
                    token_next = tokens[idx_next]
                    token_B_start += " " + token_next
                if tag_ == "B" or tag_ == "O" or idx_next == len(tags) - 1:
                    aspects.append(str(token_B_start).replace("  ", " ").strip())
                    break
            if idx_B_start == len(tags):
                aspects.append(str(token_B_start).replace("  ", " ").strip())
        # E.g. tags = ['O', 'O', 'B', 'I', 'O', 'O', 'I', 'O']
        if tag == "I":
            if idx != 0:
                idx_I_before = idx - 1
                if tags[idx_I_before] == "O":
                    aspects.append(tokens[idx])
            else:
                aspects.append(tokens[0])
    return(aspects)

def list_string_to_string(list_string):
    review = ' '.join(list_string)
    review = review.replace(" ,", ",").replace(" '", "'").replace(" .", ".")
    review = review.replace(" !", "!").replace(" ?", "?").replace(" :", ":")
    review = review.replace(" n't", "n't").replace(" 'm", "'m")
    return(review)


path_to_predictions = "./GeneratedData/"
path = path_to_predictions + "predictions.json"

predictions_punct_df = pd.read_json(path)

predictions_punct_df['Index'] = punct_reviews_for_cellPhones.Index.values
predictions_punct_df['Length'] = predictions_punct_df.idx_map.apply(len)
predictions_punct_df.head()


# Outliers
print("Num_Reviews:", len(predictions_punct_df[predictions_punct_df.Length > 100].Length.values))
print("Max_length:", max(predictions_punct_df[predictions_punct_df.Length > 100].Length.values))
ax = plt.axes()
ax.set_yscale('log')
_ = plt.hist(predictions_punct_df[predictions_punct_df.Length > 100].Length.values, bins='auto')


predictions_df_100 = predictions_punct_df[predictions_punct_df.Length < 100]
predictions_df_100 = predictions_df_100.reset_index(drop=True)

y_pred=[]
for ix, logit in enumerate(predictions_df_100["logits"]):
    pred=[0]*len(predictions_df_100["raw_X"][ix])
    #print(ix)
    for jx, idx in enumerate(predictions_df_100["idx_map"][ix]):
        #print(jx)
        lb=np.argmax(logit[jx])
        if lb==1: #B
            pred[idx]=1
        elif lb==2: #I
            if pred[idx]==0: #only when O->I (I->I and B->I ignored)
                pred[idx]=2
    y_pred.append(pred)

mapping = {0: "O", 1:"B", 2:"I"}
IOB_y_pred = []
for pred_list in y_pred:
    IOB_list = [mapping.get(item,item) for item in pred_list]
    IOB_y_pred.append(IOB_list)

predictions_df_100['tags'] = IOB_y_pred
predictions_df_100.head()

for i in range(1000):
    idx = i
    tags = predictions_df_100.tags.values[idx]
    tokens = predictions_df_100.raw_X.values[idx]
    _ = IOB_to_tokens(tags, tokens)


punct_aspect_df = pd.DataFrame()
punct_aspect_df['Index'] = predictions_df_100.Index.values

# convert list of strings to string
punct_aspect_df['Review'] = predictions_df_100.raw_X.apply(list_string_to_string).values

# convert tags to tokens
punct_aspect_df['Aspect'] = predictions_df_100.apply(lambda x: IOB_to_tokens(x.tags, x.raw_X), axis=1).values

punct_aspect_df.to_json("./punct_aspect_df.json")


punct_aspect_json_df = pd.read_json("./punct_aspect_df.json")
punct_aspect_json_df


# # **ASPECT-BASED SENTIMENT ANALYSIS:**

# **LCF: A Local Context Focus Mechanism for Aspect-Based Sentiment Classification:** [GitHub](https://github.com/songyouwei/ABSA-PyTorch)  [Paper](https://www.proquest.com/openview/a1a719bc40fffafe8c7546382a4a4d68/1?pq-origsite=gscholar&cbl=2032433)

# **1. Go to this folder: ABSA-PyTorch**
# 
# ```cd ./ABSA-PyTorch```
# 
# **2. Run the aspect-based sentiment analysis script:**
# 
# ```python3 absa.py```


punct_aspect_sentiment_json_df = pd.read_json("./punct_aspect_sentiment_df.json")
punct_aspect_sentiment_json_df


all_extracted_aspects = []
for idx, row in punct_aspect_sentiment_json_df.iterrows():
    aspect_list = row['Aspect']
    for aspect in aspect_list:
        all_extracted_aspects.append(str(aspect).lower())
all_extracted_aspects[:10]

with open('./Cellphone_all_extracted_aspects.pkl', 'wb') as fp:
    pickle.dump(all_extracted_aspects, fp, protocol=4)



from collections import Counter
from wordcloud import WordCloud
word_could_dict=Counter(all_extracted_aspects)
wordcloud = WordCloud(width = 1000, height = 500).generate_from_frequencies(word_could_dict)

plt.figure(figsize=(15,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()


aspect_frequency_sorted = {k: v for k, v in sorted(dict(word_could_dict).items(), key=lambda item: item[1], reverse=True)}
aspect_frequency_df = pd.DataFrame()
aspect_frequency_df["Aspect"] = list(aspect_frequency_sorted.keys())
aspect_frequency_df["Frequency"] = list(aspect_frequency_sorted.values())
print("Number of extracted aspects:", aspect_frequency_df.shape[0])
aspect_100 = aspect_frequency_df[aspect_frequency_df.Frequency > 99]
aspect_100


aspect_100.Aspect.values
len(aspect_100.Aspect.values)
len(list(aspect_frequency_df[aspect_frequency_df.Frequency == 1].Aspect.values))
list(aspect_frequency_df[aspect_frequency_df.Frequency == 1].Aspect.values)[:10]


def filter_aspects(row_aspect):
    valids = re.sub(r"[^A-Za-z]+", '', row_aspect)
    
    correct_aspects = ["usb", "cpu", "app", "ram", "gps", "sim", "ui", "ios", "run", "pen", "lte", "ios",
                       "mic", "sd", "os", "ask", "use", "gpu", "key", "fee", "cam", "pad", "nfc",
                       "gui", "vpn", "pay", "pic", "map", "fan", "set", "win", "buy", "tpu", "mp3", "web"]
    
    if len(valids) > 3 or valids in correct_aspects:
        return(True)
    else:
        return(False)


filtered_aspects = aspect_frequency_df.Aspect.apply(filter_aspects)
wrong_aspects_3 = list(aspect_frequency_df[~filtered_aspects].Aspect.values)

with open('./wrong_aspects_3.pkl', 'wb') as fp:
    pickle.dump(wrong_aspects_3, fp, protocol=4)


similar_aspect_list = [['android', 'android os'],
                       ['app', 'applications', 'apps', 'android apps'],
                       ['battery', 'battery life', 'batteries'],
                       ['build', 'build quality', 'built'],
                       ['button', 'buttons'],
                       ['camera', 'camera quality'],
                       ['charge', 'charger', 'charges', 'charging'],
                       ['color', 'colors'],
                       ['cost', 'costs'],
                       ['edge', 'edges'],
                       ['feature', 'features'],
                       ['front camera', 'front facing camera'],
                       ['function', 'functionality', 'functions'],
                       ['games', 'gaming'],
                       ['internal memory', 'internal storage'],
                       ['keyboard', 'keys'],
                       ['memory', 'memory card'],
                       ['operating system', 'os',],
                       ['performance', 'performs'],
                       ['power', 'power button'],
                       ['price', 'price point', 'prices'],
                       ['screen', 'screens'],
                       ['micro sd card', 'microsd card', 'sd card', 'microsd slot'],
                       ['set up', 'setup'],
                       ['sim', 'sim card'],
                       ['sound', 'sound quality'],
                       ['speaker', 'speakerphone', 'speakers'],
                       ['speed', 'speeds'],
                       ['touch screen', 'touchscreen'],
                       ['ui', 'user interface']]


aspect_filtered_100 = aspect_frequency_df[filtered_aspects][aspect_frequency_df[filtered_aspects].Frequency > 99]
aspect_filtered_100_list = list(aspect_filtered_100[aspect_filtered_100.Frequency > 99].Aspect.values)


len(aspect_filtered_100_list)


special_aspect = ['look', 'looks', 'google', 'runs', 'use', 'work', 'works']
wrong_aspects = wrong_aspects_3 + ["lumia 1020", "zero key", "verizon", 'back', 'edge', 'feel', 'phone', 'seller']
final_aspect_100_list = [aspect for aspect in aspect_filtered_100_list if aspect not in wrong_aspects]


sentiments = {0: 'Negative', 1: "Neutral", 2: 'Positive', -999: ''}
def sentiment_aspect_dict(index, review, aspect_list, polarity_list, 
                          polarity_score_list, sentiments, final_aspect_100_list, polarity_treshold = 0.8):
    absa_dictionary = {}    
    if aspect_list:
        for counter, aspect in enumerate(aspect_list):
            if aspect in final_aspect_100_list:
                polarity_scores = polarity_score_list[counter][0]
                if max(polarity_scores) >= polarity_treshold:
                    new_index = str(index) + "_" + str(counter)
                    absa_dictionary[(new_index, aspect)] = {}
                    absa_dictionary[(new_index, aspect)]['review'] = review
                    polarity_idx = polarity_list[counter][0]
                    absa_dictionary[(new_index, aspect)]['polarity'] = sentiments[polarity_idx]
                    polarity_scores = polarity_score_list[counter][0]
                    absa_dictionary[(new_index, aspect)]['polarity_scores'] = polarity_scores
    return(absa_dictionary)

sentiment_aspect_dict_all = {}
for idx, row in punct_aspect_sentiment_json_df.iterrows():
    if idx%1000 == 0:
        print(idx)
    all_index_list = row['Index'].split("_")
    item = str(all_index_list[0])
    
    index = row['Index'] 
    review = row['Review']
    aspect_list = row['Aspect']
    polarity_list = row['Polarity']
    polarity_score_list = row['Polarity_score']
    
    absa_dict_result = sentiment_aspect_dict(index, review, aspect_list, polarity_list, 
                                             polarity_score_list, sentiments, final_aspect_100_list, polarity_treshold = 0.8)
    if absa_dict_result:
        if item not in sentiment_aspect_dict_all:
            sentiment_aspect_dict_all[item] = []
            sentiment_aspect_dict_list = sentiment_aspect_dict_all[item]
            sentiment_aspect_dict_list.append(absa_dict_result)
        else:
            sentiment_aspect_dict_list = sentiment_aspect_dict_all[item]
            sentiment_aspect_dict_list.append(absa_dict_result)


with open('./Cellphone_similar_aspect_list_100.pkl', 'wb') as fp:
    pickle.dump(similar_aspect_list, fp, protocol=4)
    
with open('./Cellphone_sentiment_aspect_dict_100.pkl', 'wb') as fp:
    pickle.dump(sentiment_aspect_dict_all, fp, protocol=4)


english_vocab = pd.read_pickle("./english_vocab.pkl")
stop_words = pd.read_pickle("./stop_words.pkl")
wrong_aspects_3 = pd.read_pickle('./wrong_aspects_3.pkl')
metaData_for_cellPhones = pd.read_pickle("./metaData_for_cellPhones.pkl")
dict_AspectSentiment = pd.read_pickle('./Cellphone_sentiment_aspect_dict_100.pkl')

with open(".../Data/GeneratedData/retrieved_items_dict.json") as f:
    retrieved_items_dict = json.load(f)

wrong_aspects = wrong_aspects_3 + ["lumia 1020", "zero key", "verizon", 'back', 'edge', 'feel', 'phone', 'seller']

correct_forms = ['bluetooth']


def aspects_similarity_check(aspect_1, aspect_2, similar_aspect_list):
    check=False
    for i in similar_aspect_list:
        if aspect_1.lower() in i and aspect_2.lower() in i:
            check=True
            break
    if check:
        return(True)
    else:
        return(False)

def cleaning_aspect(aspect):
    if aspect != None:
        cleaned_aspect = aspect.replace("/", "")
        cleaned_aspect = re.sub(' +', ' ', cleaned_aspect)
        cleaned_aspect = cleaned_aspect.strip()
    else:
        cleaned_aspect = aspect
    return(cleaned_aspect)

def cleaning_review(review):
    if str(review).lower()[:3].strip() == "but":
        cleaned_review = str(review)[3:].strip(":")
        cleaned_review = cleaned_review.strip(";")
        cleaned_review = cleaned_review.strip(",")
        cleaned_review = cleaned_review.strip()
    elif str(review).lower()[:3].strip() == "and":
        cleaned_review = str(review)[3:].strip(":")
        cleaned_review = cleaned_review.strip(";")
        cleaned_review = cleaned_review.strip(",")
        cleaned_review = cleaned_review.strip()
    elif str(review).lower()[:4].strip() == "then":
        cleaned_review = str(review)[4:].strip(":")
        cleaned_review = cleaned_review.strip(";")
        cleaned_review = cleaned_review.strip(",")
        cleaned_review = cleaned_review.strip()
    elif str(review).lower()[:9].strip() == "otherwise":
        cleaned_review = str(review)[9:].strip(":")
        cleaned_review = cleaned_review.strip(";")
        cleaned_review = cleaned_review.strip(",")
        cleaned_review = cleaned_review.strip()
    else:
        cleaned_review = review
    return(cleaned_review)


metaData_for_cellPhones = pd.read_pickle("./metaData_for_cellPhones.pkl")




done_items_neg = []
all_blocks_neg = {}

for index in list(retrieved_items_dict.keys()):
    print(str(index))
    retrieved_items_1 = retrieved_items_dict[str(index)].get("retrieved items")
    retrieved_items_with_review = [i for i in retrieved_items_1 if metaData_for_cellPhones.query("asin == @i").num_reviews.values[0] > 0]
    print('retrieved_items_with_review:', retrieved_items_with_review)
    if len(retrieved_items_with_review) > 0:
        for item in retrieved_items_with_review:
            if item not in done_items_neg:
                done_items_neg.append(item)
                print(item)
                all_blocks_neg[str(item)] = {}
                blocks_Qpos1A_Apos1A = Qpos1A_Apos1A(item, wrong_aspects, correct_forms, Q1A_list, dict_AspectSentiment)
                all_blocks_neg[str(item)]['Qpos1A_Apos1A'] = blocks_Qpos1A_Apos1A
                print("blocks_Qpos1A_Apos1A is DONE!")
                
                blocks_Oneg1A_Opos1A = Oneg1A_Opos1A(item, wrong_aspects, correct_forms, Oneg1A_list, Opos1A_list, dict_AspectSentiment)
                all_blocks_neg[str(item)]['Oneg1A_Opos1A'] = blocks_Oneg1A_Opos1A
                print("blocks_Oneg1A_Opos1A is DONE!")

                blocks_Oneg1A_Opos1B_retrieved = Oneg1A_Opos1B(item, retrieved_items_with_review, wrong_aspects, correct_forms, Oneg1A_list, Opos1B_list,
                                                     dict_AspectSentiment, metaData_for_cellPhones, retrieved=True, also_view=False)
                all_blocks_neg[str(item)]['Oneg1A_Opos1B_retrieved'] = blocks_Oneg1A_Opos1B_retrieved
                print("blocks_Oneg1A_Opos1B_retrieved is DONE!")

                blocks_Oneg1A_Opos1B_also_view = Oneg1A_Opos1B(item, retrieved_items_with_review, wrong_aspects, correct_forms, Oneg1A_list, Opos1B_list,
                                                     dict_AspectSentiment, metaData_for_cellPhones, retrieved=False, also_view=True)
                all_blocks_neg[str(item)]['Oneg1A_Opos1B_also_view'] = blocks_Oneg1A_Opos1B_also_view
                print("blocks_Oneg1A_Opos1B_also_view is DONE!")

                blocks_Oneg1A_Opos2A_restricted = Oneg1A_Opos2A(item, wrong_aspects, correct_forms, Oneg1A_list, Opos2A_list,
                                                    dict_AspectSentiment, restricted_version=True)
                all_blocks_neg[str(item)]['Oneg1A_Opos2A_restricted'] = blocks_Oneg1A_Opos2A_restricted
                print("blocks_Oneg1A_Opos2A_restricted is DONE!")
                
                blocks_Oneg1A_Opos2A_unrestricted = Oneg1A_Opos2A(item, wrong_aspects, correct_forms, Oneg1A_list, Opos2A_list,
                                                                  dict_AspectSentiment, restricted_version=False)
                all_blocks_neg[str(item)]['Oneg1A_Opos2A_unrestricted'] = blocks_Oneg1A_Opos2A_unrestricted
                print("blocks_Oneg1A_Opos2A_unrestricted is DONE!")

with open('./100_blocks_neg.json', 'w') as f:
    json.dump(all_blocks_neg, f)

with open('./done_items_neg.pkl', 'wb') as fp:
    pickle.dump(done_items_neg, fp, protocol=4)


def Opos1B_Opos2B(item, wrong_aspects, correct_forms, Opos1B1_list, Opos2B_list, dict_AspectSentiment):
    blocks = {}
    counter = 0
    similarity = 0
    aspect_review_polarity_key_list = []
    item_review_list = dict_AspectSentiment.get(item)
    if item_review_list:
        for review_dict in item_review_list:
            for item_reviewer_aspect_key, review_sentiment in (review_dict.items()):
                key = item_reviewer_aspect_key[0]
                aspect = item_reviewer_aspect_key[1]
                aspect = cleaning_aspect(aspect)
                review = review_sentiment['review']
                review = cleaning_review(review)
                polarity = review_sentiment['polarity']
                if aspect not in wrong_aspects and aspect != None:
                    if str(polarity).lower() == 'positive':
                        aspect_review_polarity_key_list.append((aspect, review, polarity, key))
                        
    if item_review_list:
        for review_dict in item_review_list:
            for item_reviewer_aspect_key, review_sentiment in (review_dict.items()):
                key = item_reviewer_aspect_key[0]
                aspect = item_reviewer_aspect_key[1]
                aspect = cleaning_aspect(aspect)
                review = review_sentiment['review']
                review = cleaning_review(review)
                polarity = review_sentiment['polarity']
                if aspect != None and aspect not in wrong_aspects:
                    if str(polarity).lower() == 'positive':
                        
                        sentence_aspect = review
                        
                        #For MultiWOZ
                        #Opos1B = random.choice(Opos1B1_list).format(aspect) + sentence_aspect
                        Opos1B = random.choice(Opos1B1_list).format(item, aspect) + sentence_aspect
    
                        for aspect_, review_, polarity_, key_ in aspect_review_polarity_key_list:
                            aspect_ = cleaning_aspect(aspect_)
                            if str(polarity_).lower() == 'positive' and str(review) != str(review_):
                                counter += 1

                                sentence_aspect_ = review_

                                Opos2B = random.choice(Opos2B_list).format(aspect_) + sentence_aspect_

                                blocks["Opos1B_Opos2B_" + str(counter)] = {}
                                blocks["Opos1B_Opos2B_" + str(counter)]['Opos1B'] = {}
                                blocks["Opos1B_Opos2B_" + str(counter)]['Opos1B']['Opinion'] = Opos1B
                                blocks["Opos1B_Opos2B_" + str(counter)]['Opos1B']['Labels'] = {}
                                blocks["Opos1B_Opos2B_" + str(counter)]['Opos1B']['Labels']['Key'] = key
                                blocks["Opos1B_Opos2B_" + str(counter)]['Opos1B']['Labels']['Aspect'] = aspect
                                blocks["Opos1B_Opos2B_" + str(counter)]['Opos1B']['Labels']['Polarity'] = str(polarity).lower()

                                blocks["Opos1B_Opos2B_" + str(counter)]['Opos2B'] = {}
                                blocks["Opos1B_Opos2B_" + str(counter)]['Opos2B']['Opinion'] = Opos2B
                                blocks["Opos1B_Opos2B_" + str(counter)]['Opos2B']['Labels'] = {}
                                blocks["Opos1B_Opos2B_" + str(counter)]['Opos2B']['Labels']['Key'] = key_
                                blocks["Opos1B_Opos2B_" + str(counter)]['Opos2B']['Labels']['Aspect'] = aspect_
                                blocks["Opos1B_Opos2B_" + str(counter)]['Opos2B']['Labels']['Polarity'] = str(polarity_).lower()
    return(blocks)

def Opos1B_Opos1B2(item, wrong_aspects, correct_forms, Opos1B1_list, Opos1B2_list,
                  dict_AspectSentiment, only_agreement=True, agreement_and_more=True):
    blocks = {}
    counter = 0
    similarity = 0
    aspect_review_polarity_key_list = []
    item_review_list = dict_AspectSentiment.get(item)
    if item_review_list and agreement_and_more:
        for review_dict in item_review_list:
            for item_reviewer_aspect_key, review_sentiment in (review_dict.items()):
                key = item_reviewer_aspect_key[0]
                aspect = item_reviewer_aspect_key[1]
                aspect = cleaning_aspect(aspect)
                review = review_sentiment['review']
                review = cleaning_review(review)
                polarity = review_sentiment['polarity']
                if aspect not in wrong_aspects and aspect != None:
                    if str(polarity).lower() == 'positive':
                        aspect_review_polarity_key_list.append((aspect, review, polarity, key))
                        
    if item_review_list:
        for review_dict in item_review_list:
            for item_reviewer_aspect_key, review_sentiment in (review_dict.items()):
                key = item_reviewer_aspect_key[0]
                aspect = item_reviewer_aspect_key[1]
                aspect = cleaning_aspect(aspect)
                review = review_sentiment['review']
                review = cleaning_review(review)
                polarity = review_sentiment['polarity']
                if aspect != None and aspect not in wrong_aspects:
                    if str(polarity).lower() == 'positive':
                        
                        #For MultiWOZ
                        #Opos1B = random.choice(Opos1B1_list).format(aspect) + sentence_aspect
                        Opos1B = random.choice(Opos1B1_list).format(item, aspect) + review
                        
                        if only_agreement:
                            counter += 1
                            
                            Opos1B2 = random.choice(Opos1B2_list)
                            
                            blocks["Opos1B_Opos1B2_" + str(counter)] = {}
                            blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B'] = {}
                            blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B']['Opinion'] = Opos1B
                            blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B']['Labels'] = {}
                            blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B']['Labels']['Key'] = key
                            blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B']['Labels']['Aspect'] = aspect
                            blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B']['Labels']['Polarity'] = str(polarity).lower()

                            blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B2'] = {}
                            blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B2']['Opinion'] = Opos1B2
                            blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B2']['Labels'] = {}
                            blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B2']['Labels']['Key'] = key
                            blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B2']['Labels']['Aspect'] = aspect
                            blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B2']['Labels']['Polarity'] = str(polarity).lower()
                            
                        elif agreement_and_more:
                            
                            for aspect_, review_, polarity_, key_ in aspect_review_polarity_key_list:
                                aspect_ = cleaning_aspect(aspect_)

                                if np.logical_or(aspect == aspect_, aspects_similarity_check(aspect, aspect_, similar_aspect_list)) and str(review_) != str(review):  
                                    counter += 1

                                    Opos1B2 = random.choice(Opos1B2_list) + " " + review_

                                    blocks["Opos1B_Opos1B2_" + str(counter)] = {}
                                    blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B'] = {}
                                    blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B']['Opinion'] = Opos1B
                                    blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B']['Labels'] = {}
                                    blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B']['Labels']['Key'] = key
                                    blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B']['Labels']['Aspect'] = aspect
                                    blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B']['Labels']['Polarity'] = str(polarity).lower()

                                    blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B2'] = {}
                                    blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B2']['Opinion'] = Opos1B2
                                    blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B2']['Labels'] = {}
                                    blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B2']['Labels']['Key'] = key_
                                    blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B2']['Labels']['Aspect'] = aspect_
                                    blocks["Opos1B_Opos1B2_" + str(counter)]['Opos1B2']['Labels']['Polarity'] = str(polarity_).lower()
    return(blocks)

def Opos1B_Oneg2B(item, wrong_aspects, correct_forms, Opos1B1_list, Oneg2B_list, dict_AspectSentiment):
    blocks = {}
    counter = 0
    similarity = 0
    aspect_review_polarity_key_list = []
    item_review_list = dict_AspectSentiment.get(item)
    if item_review_list:
        for review_dict in item_review_list:
            for item_reviewer_aspect_key, review_sentiment in (review_dict.items()):
                key = item_reviewer_aspect_key[0]
                aspect = item_reviewer_aspect_key[1]
                aspect = cleaning_aspect(aspect)
                review = review_sentiment['review']
                review = cleaning_review(review)
                polarity = review_sentiment['polarity']
                if aspect not in wrong_aspects and aspect != None:
                    if str(polarity).lower() == 'negative':
                        aspect_review_polarity_key_list.append((aspect, review, polarity, key))
                        
    if item_review_list:
        for review_dict in item_review_list:
            for item_reviewer_aspect_key, review_sentiment in (review_dict.items()):
                key = item_reviewer_aspect_key[0]
                aspect = item_reviewer_aspect_key[1]
                aspect = cleaning_aspect(aspect)
                review = review_sentiment['review']
                review = cleaning_review(review)
                polarity = review_sentiment['polarity']
                if aspect != None and aspect not in wrong_aspects:
                    if str(polarity).lower() == 'positive':
                        
                        #For MultiWOZ
                        #Opos1B = random.choice(Opos1B1_list).format(aspect) + sentence_aspect
                        Opos1B = random.choice(Opos1B1_list).format(item, aspect) + review
    
                        for aspect_, review_, polarity_, key_ in aspect_review_polarity_key_list:
                            aspect_ = cleaning_aspect(aspect_)

                            if str(polarity_).lower() == 'negative' and str(review) != str(review_): 
                                counter += 1

                                Oneg2B = random.choice(Oneg2B_list).format(aspect_) + review_

                                blocks["Opos1B_Oneg2B_" + str(counter)] = {}
                                blocks["Opos1B_Oneg2B_" + str(counter)]['Opos1B'] = {}
                                blocks["Opos1B_Oneg2B_" + str(counter)]['Opos1B']['Opinion'] = Opos1B
                                blocks["Opos1B_Oneg2B_" + str(counter)]['Opos1B']['Labels'] = {}
                                blocks["Opos1B_Oneg2B_" + str(counter)]['Opos1B']['Labels']['Key'] = key
                                blocks["Opos1B_Oneg2B_" + str(counter)]['Opos1B']['Labels']['Aspect'] = aspect
                                blocks["Opos1B_Oneg2B_" + str(counter)]['Opos1B']['Labels']['Polarity'] = str(polarity).lower()

                                blocks["Opos1B_Oneg2B_" + str(counter)]['Oneg2B'] = {}
                                blocks["Opos1B_Oneg2B_" + str(counter)]['Oneg2B']['Opinion'] = Oneg2B
                                blocks["Opos1B_Oneg2B_" + str(counter)]['Oneg2B']['Labels'] = {}
                                blocks["Opos1B_Oneg2B_" + str(counter)]['Oneg2B']['Labels']['Key'] = key_
                                blocks["Opos1B_Oneg2B_" + str(counter)]['Oneg2B']['Labels']['Aspect'] = aspect_
                                blocks["Opos1B_Oneg2B_" + str(counter)]['Oneg2B']['Labels']['Polarity'] = str(polarity_).lower()
    return(blocks)

done_items_pos = []
all_blocks_pos = {}
for index in list(retrieved_items_dict.keys()):
    print(str(index))
    retrieved_items_1 = retrieved_items_dict[str(index)].get("retrieved items")
    retrieved_items_with_review = [i for i in retrieved_items_1 if metaData_for_cellPhones.query("asin == @i").num_reviews.values[0] > 0]
    print('retrieved_items_with_review:', retrieved_items_with_review)
    if len(retrieved_items_with_review) > 0:
        for item in retrieved_items_with_review:
            if item not in all_blocks_pos:
                print(item)
                done_items_pos.append(item)
                all_blocks_pos[str(item)] = {}               
                blocks_Opos1B_Opos1B2_only_agreement = Opos1B_Opos1B2(item, wrong_aspects, correct_forms, Opos1B1_list, Opos1B2_list,
                                                          dict_AspectSentiment, only_agreement=True, agreement_and_more=False)
                all_blocks_pos[str(item)]['Opos1B_Opos1B2_only_agreement'] = blocks_Opos1B_Opos1B2_only_agreement
                print("Opos1B_Opos1B2_only_agreement is DONE!")

                blocks_Opos1B_Opos1B2_agreement_and_more = Opos1B_Opos1B2(item, wrong_aspects, correct_forms, Opos1B1_list, Opos1B2_list,
                                                                          dict_AspectSentiment, only_agreement=False, agreement_and_more=True)
                all_blocks_pos[str(item)]['Opos1B_Opos1B2_agreement_and_more'] = blocks_Opos1B_Opos1B2_agreement_and_more
                print("blocks_Opos1B_Opos1B2_agreement_and_more is DONE!")

                blocks_Opos1B_Opos2B = Opos1B_Opos2B(item, wrong_aspects, correct_forms, Opos1B1_list, Opos2B_list, dict_AspectSentiment)
                all_blocks_pos[str(item)]['Opos1B_Opos2B'] = blocks_Opos1B_Opos2B
                print("blocks_Opos1B_Opos2B is DONE!")

                blocks_Opos1B_Oneg2B = Opos1B_Oneg2B(item, wrong_aspects, correct_forms, Opos1B1_list, Oneg2B_list, dict_AspectSentiment)
                all_blocks_pos[str(item)]['Opos1B_Oneg2B'] = blocks_Opos1B_Oneg2B
                print("blocks_Opos1B_Oneg2B is DONE!")

with open('./100_blocks_pos.json', 'w') as f:
    json.dump(all_blocks_pos, f)

with open('./done_items_pos.pkl', 'wb') as fp:
    pickle.dump(done_items_pos, fp, protocol=4)


# # **GENERATING CONVERSATIONS:**


with open('./100_blocks_neg.json') as f:
    blocks_neg_100 = json.load(f)

with open('./100_blocks_pos.json') as f:
    blocks_pos_100 = json.load(f)



with open("./retrieved_items_dict.json") as f:
    retrieved_items_dict = json.load(f)
    
metaData_for_cellPhones = pd.read_pickle("./metaData_for_cellPhones.pkl")

all_items_with_review = []
for index in list(retrieved_items_dict.keys()):
    retrieved_items_1 = retrieved_items_dict[str(index)].get("retrieved items")
    retrieved_items_with_review = [i for i in retrieved_items_1 if metaData_for_cellPhones.query("asin == @i").num_reviews.values[0] > 0]
    all_items_with_review += retrieved_items_with_review
    
all_items_with_review = list(set(all_items_with_review))

def find_retrieved_items_and_index(retrieved_items_dict, selected_item):
    all_retrieved_index = []
    all_retrieved_items = []
    for index in range(1, len(retrieved_items_dict.keys())+1):
        retrieved_items_list = retrieved_items_dict[str(index)].get("retrieved items")
        if selected_item in retrieved_items_list:
            all_retrieved_index.append(index)
            all_retrieved_items += retrieved_items_dict[str(index)].get("retrieved items")
    all_retrieved_items = list(set(all_retrieved_items))
    return(all_retrieved_index, all_retrieved_items)

def select_pairs_combination(all_pairs_combination, num_pairs):
    selected_pairs_combination = []
    if len(all_pairs_combination) > num_pairs:
        for i in range(5):
            random.shuffle(all_pairs_combination)
        while len(selected_pairs_combination) < num_pairs:
            selected_pair_combination = random.choice(all_pairs_combination)
            if selected_pair_combination not in selected_pairs_combination:
                selected_pairs_combination.append(selected_pair_combination)
    else:
        selected_pairs_combination = all_pairs_combination
    return(selected_pairs_combination)


# ### Generate Dataset

dataset = {}
num_pairs = 50
for item_counter, item in enumerate(all_items_with_review):
    print(item_counter + 1)
    dataset[str(item)] = {}
    conv_type_1_dict = conv_type_1(str(item), num_pairs)
    dataset[str(item)]['conv_type_1'] = conv_type_1_dict
    conv_type_2_dict = conv_type_2(str(item), num_pairs)
    dataset[str(item)]['conv_type_2'] = conv_type_2_dict
    conv_type_3_dict = conv_type_3(str(item), num_pairs)
    dataset[str(item)]['conv_type_3'] = conv_type_3_dict
    conv_type_4_dict = conv_type_4(str(item), num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict)
    dataset[str(item)]['conv_type_4'] = conv_type_4_dict
    conv_type_5_dict = conv_type_5(str(item), num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict)
    dataset[str(item)]['conv_type_5'] = conv_type_5_dict
    conv_type_6_dict = conv_type_6(str(item), num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict)
    dataset[str(item)]['conv_type_6'] = conv_type_6_dict
    conv_type_7_dict = conv_type_7(str(item), num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict)
    dataset[str(item)]['conv_type_7'] = conv_type_7_dict
    conv_type_8_dict = conv_type_8(str(item), num_pairs)
    dataset[str(item)]['conv_type_8'] = conv_type_8_dict
    conv_type_9_dict = conv_type_9(str(item), num_pairs)
    dataset[str(item)]['conv_type_9'] = conv_type_9_dict
    conv_type_10_dict = conv_type_10(str(item), num_pairs)
    dataset[str(item)]['conv_type_10'] = conv_type_10_dict
    conv_type_11_dict = conv_type_11(str(item), num_pairs)
    dataset[str(item)]['conv_type_11'] = conv_type_11_dict
    conv_type_12_dict = conv_type_12(str(item), num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict)
    dataset[str(item)]['conv_type_12'] = conv_type_12_dict
    conv_type_13_dict = conv_type_13(str(item), num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict)
    dataset[str(item)]['conv_type_13'] = conv_type_13_dict
    conv_type_14_dict = conv_type_14(str(item), num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict)
    dataset[str(item)]['conv_type_14'] = conv_type_14_dict


with open('dataset.json', 'w') as f:
    json.dump(dataset, f)

