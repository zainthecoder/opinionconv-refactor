from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

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

### load the data
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
