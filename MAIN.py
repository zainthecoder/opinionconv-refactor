import pandas as pd
import numpy as np
import json
import re
import itertools
import pickle
import logging
import copy
import pprint

import pprint

import os


from datasets import load_dataset


def extract_brand(details):
    if isinstance(details, str):  # Check if details is a string
        try:
            details_dict = json.loads(details)  # Convert string to dictionary
            return details_dict.get("Brand", None)  # Extract 'Brand' if exists
        except json.JSONDecodeError:
            return None  # Return None if there's a problem with JSON parsing
    return None


# # **LOAD AMAZON DATASETS:**


df_metaData_raw_cellPhones = load_dataset(
    "McAuley-Lab/Amazon-Reviews-2023",
    "raw_meta_Cell_Phones_and_Accessories",
    split="full",
    trust_remote_code=True,
)

df_metaData_raw_cellPhones = df_metaData_raw_cellPhones.to_pandas()

df_metaData_raw_cellPhones["brand"] = df_metaData_raw_cellPhones["details"].apply(
    extract_brand
)
# Reviews


df_review_raw_cellPhones = load_dataset(
    "McAuley-Lab/Amazon-Reviews-2023",
    "raw_review_Cell_Phones_and_Accessories",
    split="full",
    trust_remote_code=True,
)
print("##")
print("df_review_raw_cellPhones")
print("##")
print("1")
# pprint.pprint(df_review_raw_cellPhones[0:2])
df_review_raw_cellPhones = df_review_raw_cellPhones.to_pandas()


# # ### **3. Ratings**


df_ratings_raw_cellPhones = load_dataset(
    "McAuley-Lab/Amazon-Reviews-2023",
    "5core_rating_only_Cell_Phones_and_Accessories",
    split="full",
    trust_remote_code=True,
)

print("##")
print("df_ratings_raw_cellPhones")
print("##")
pprint.pprint(df_ratings_raw_cellPhones[0:2])
df_ratings_raw_cellPhones = df_ratings_raw_cellPhones.to_pandas()


df_ratings_raw_cellPhones["timestamp"] = pd.to_datetime(
    df_ratings_raw_cellPhones["timestamp"], unit="s", errors="coerce"
)


# Filter items with less than 6 categories & Split column of lists into multiple columns
df_metaData_raw_cellPhones_c1 = df_metaData_raw_cellPhones[
    df_metaData_raw_cellPhones.categories.map(len) < 6
]
df_categories_cellPhones = pd.DataFrame(
    df_metaData_raw_cellPhones_c1["categories"].values.tolist()
).add_prefix("category_")

df_metaData_concat_cellPhones = pd.concat(
    [
        df_categories_cellPhones.reset_index(drop=True),
        df_metaData_raw_cellPhones_c1.reset_index(drop=True),
    ],
    axis=1,
)

# Remove items without price
price_df_metaData_cellPhones = df_metaData_concat_cellPhones[
    df_metaData_concat_cellPhones.price != ""
]
price_df_metaData_cellPhones = df_metaData_concat_cellPhones[
    df_metaData_concat_cellPhones.price != "None"
]
# Remove items with wrong extracted price
price_df_metaData_cellPhones = price_df_metaData_cellPhones[
    price_df_metaData_cellPhones.price.str.len() < 9
]

print(price_df_metaData_cellPhones[0:3]["price"])

# Remove dollar ($) sign for sorting
price_df_metaData_cellPhones["price"] = price_df_metaData_cellPhones["price"].replace(
    "—", np.nan
)
price_df_metaData_cellPhones["price"] = price_df_metaData_cellPhones.price.str.replace(
    "$", ""
).astype(float)


# Remove duplicates
subset = [
    "category_0",
    "category_1",
    "category_2",
    "category_3",
    "main_category",
    "title",
    "average_rating",
    "rating_number",
    "features",
    "description",
    "price",
    "images",
    "videos",
    "store",
    "categories",
    "details",
    "parent_asin",
    "bought_together",
    "subtitle",
    "author"
]


df_metaData_cellPhones = price_df_metaData_cellPhones.loc[
    price_df_metaData_cellPhones.astype(str)
    .drop_duplicates(subset=subset, keep="first", inplace=False)
    .index
]


# print(df_metaData_cellPhones["main_category"].unique())
# print(df_metaData_cellPhones["category_0"].unique())
# print(df_metaData_cellPhones["category_1"].unique())
# print(df_metaData_cellPhones["category_2"].unique())

# Add rating


# Assuming df_ratings_raw_cellPhones is your DataFrame
df_ratings_raw_cellPhones["rating"] = df_ratings_raw_cellPhones["rating"].astype(float)


print("GroupBy")
df_ratings_cellPhones = df_ratings_raw_cellPhones.groupby(by="parent_asin").agg(
    num_ratings=("rating", "count"), sum_ratings=("rating", "sum")
)

df_ratings_cellPhones["avg_rating"] = (
    df_ratings_cellPhones.sum_ratings / df_ratings_cellPhones.num_ratings
)
df_ratings_cellPhones["asin"] = df_ratings_cellPhones.index
print("df_ratings_cellPhones")
print(df_ratings_cellPhones.head())


# Merge df_metaData and df_ratings
df_metaData_ratings_cellPhones = pd.merge(
    df_metaData_cellPhones, df_ratings_cellPhones, on="parent_asin"
)
df_metaData_ratings_cellPhones.head()


# Filter the items which have "Cell Phones" in category_1 and the main_category == "Cell Phones & Accessories"
Cell_Phones_df_raw = df_metaData_ratings_cellPhones[
    df_metaData_ratings_cellPhones.main_category == "Cell Phones & Accessories"
]
print("main category filter")
pprint.pprint(Cell_Phones_df_raw.head())

Cell_Phones_df_raw = Cell_Phones_df_raw[Cell_Phones_df_raw.category_1 == "Cell Phones"]
print("category 0 filter")
pprint.pprint(Cell_Phones_df_raw.head())
# Useful Cols
subset_cols = [
    "category_0",
    "category_1",
    "category_2",
    "category_3",
    "description",
    "title",
    "bought_together",
    "images",
    "features",
    "details",
    "main_category",
    "price",
    "num_ratings",
    "avg_rating",
    "asin",
    "parent_asin",
    "brand",
]

Cell_Phones_df_raw = Cell_Phones_df_raw[subset_cols]
Cell_Phones_df_raw.reset_index(drop=True, inplace=True)

# Merging 3 columns: description, feature & title
all_features = Cell_Phones_df_raw[["description", "features", "title"]].values.tolist()
col_all_features = []
for i in all_features:
    list_features = []
    for j in i:
        if j is not None:
            if type(j) == list:
                for k in j:
                    list_features.append(str(k))
            else:
                list_features.append(str(j))
    col_all_features.append(" ****** ".join(list_features))

Cell_Phones_df_raw["all_features"] = col_all_features

print("merging 3 columns")
pprint.pprint(Cell_Phones_df_raw.head())


# Define the list of DataFrames for the brands you want to remove
remove_brand_list = [
    Cell_Phones_df_raw[Cell_Phones_df_raw.brand == "OtterBox"],
    Cell_Phones_df_raw[Cell_Phones_df_raw.brand == "Saunders"],
    Cell_Phones_df_raw[Cell_Phones_df_raw.brand == "F FORITO"],
]

# Initialize empty lists for indices and ASINs to be removed
remove_indices = []
remove_asin = []

# Iterate over the list of DataFrames and collect indices and ASINs
for remove_df in remove_brand_list:
    remove_indices.extend(remove_df.index.values)  # Append indices directly to the list
    remove_asin.extend(remove_df.asin.values)  # Append ASINs directly to the list

# Drop the rows using the indices
Cell_Phones_df_raw.drop(remove_indices, axis=0, inplace=True)


# Replace wrong brands
replace_brand_lists = [
    [["Unknown"], ["BlackBerry", "Alcatel", "LG", "LG"]],
    [["AT&T"], ["ZTE", "Huawei", "ZTE", "ZTE", "ZTE", "ZTE"]],
    [["Nexus"], ["Motorola", "Google"]],
    [
        ["Tracfone"],
        ["Motorola", "Alcatel", "LG", "Alcatel", "ZTE", "LG", "LG", "Motorola"],
    ],
    [["FreedomPop"], ["Samsung", "Samsung", "Samsung", "Motorola"]],
    [
        [""],
        [
            "Alcatel",
            "BLU",
            "Samsung",
            "Motorola",
            "LG",
            "LG",
            "Kyocera",
            "LG",
            "Alcatel",
            "T-Mobile",
            "Sony",
            "LG",
            "Letv",
            "Yotaphone",
            "T-Mobile",
            "Pantech",
            "LG",
            "Google",
        ],
    ],
    [["Blackberry"], ["BlackBerry"]],
    [["Net10"], ["ZTE", "Huawei"]],
    [["Sanyo 8400"], ["Sanyo"]],
    [["Nextel"], ["Motorola"]],
    [["Sprint"], ["Sanyo"]],
    [["LGIC"], ["LG"]],
    [["Verizon"], ["Samsung"]],
    [["DCP Products"], ["Pantech"]],
    [["Caterpillar"], ["Cat"]],
    [["Tellme"], ["Emporia"]],
    [["Boost Mobile"], ["Kyocera"]],
    [["P710"], ["LG"]],
    [["ZTE USA"], ["ZTE"]],
    [["NET10"], ["LG"]],
    [["T Mobile"], ["Alcatel"]],
    [["MOTCB"], ["Motorola"]],
    [["TRACFONE WIRELESS, INC."], ["LG"]],
    [["Samsung Korea"], ["Samsung"]],
    [["Quality One Wireless"], ["Alcatel"]],
    [["Porsche Design"], ["BlackBerry"]],
    [["Moto X"], ["Motorola"]],
    [["Thailand"], ["THL"]],
    [["INEW"], ["Samsung"]],
    [["OneTouch"], ["Alcatel"]],
    [["VOWSVOWS"], ["BLU"]],
    [["ASUS"], ["Asus"]],
    [["Galaxy S5"], ["Samsung"]],
    [["Samsung/Straight Talk"], ["Samsung"]],
    [["SoonerSoft Electronics"], ["LG"]],
    [["CAT PHONES"], ["Cat"]],
    [["Samsung Group"], ["Samsung"]],
    [["Peirui"], ["OnePlus"]],
    [["CT-Miami LLC"], ["BLU"]],
    [["iGearPro"], ["Samsung"]],
    [["Pixi"], ["Alcatel"]],
    [["Risio"], ["LG"]],
]


def replace_wrong_brands(replace_brand_lists, df):
    df = df.copy()

    for replace_brand_list in replace_brand_lists:
        wrong_brand = replace_brand_list[0][0]
        correct_brands = replace_brand_list[1]

        # Get rows where the brand is incorrect
        incorrect_df = df[df.brand == wrong_brand]
        incorrect_df_asin = incorrect_df.asin.values

        # Case 1: More than one correct brand
        if len(correct_brands) > 1:
            # If there are more incorrect brands than correct ones, cycle through correct brands
            correct_brands_extended = (
                correct_brands * ((len(incorrect_df_asin) // len(correct_brands)) + 1)
            )[: len(incorrect_df_asin)]

            for i in range(len(incorrect_df_asin)):
                asin_ = incorrect_df_asin[i]
                brand_ = correct_brands_extended[i]
                index = df.query("asin == @asin_").index.values[0]
                df.loc[index, "brand"] = brand_

        # Case 2: Only one correct brand, apply it to all incorrect entries
        elif len(correct_brands) == 1:
            brand_ = correct_brands[0]
            indices = incorrect_df.index.values
            df.loc[indices, "brand"] = brand_

    return df


# Applying the function to your DataFrame
Cell_Phones_df = replace_wrong_brands(
    replace_brand_lists=replace_brand_lists, df=Cell_Phones_df_raw
)

print("after replacing bad brands")
pprint.pprint(Cell_Phones_df.head())


# Adding numnber of reviews
#if not os.path.exists("./metaData_for_cellPhones.pkl"):
reviews_for_cellPhones = df_review_raw_cellPhones.loc[
    df_review_raw_cellPhones["asin"].isin(Cell_Phones_df.asin.unique())
]
df_asin_numReviews = pd.DataFrame()
df_asin_numReviews["asin"] = (
    reviews_for_cellPhones.groupby(by="asin").count()[["text"]].index
)
df_asin_numReviews["num_reviews"] = (
    reviews_for_cellPhones.groupby(by="asin").count()[["text"]].text.values
)

metaData_for_cellPhones = Cell_Phones_df.merge(
    df_asin_numReviews, on="asin", how="outer"
)
metaData_for_cellPhones.fillna(value=0, inplace=True)

metaData_for_cellPhones.head(3)

with open("./metaData_for_cellPhones.pkl", "wb") as fp:
    pickle.dump(metaData_for_cellPhones, fp, protocol=4)
# else:
#     print("MIL GAYA")


def cleaning_process(text):
    cleaned_text = text.replace("\n\n", " ")
    cleaned_text = cleaned_text.replace("\n", " ")
    cleaned_text = cleaned_text.replace("#", " ")
    cleaned_text = cleaned_text.replace("*", " ")
    cleaned_text = cleaned_text.replace("+", " ")
    cleaned_text = cleaned_text.replace("'", "'")
    cleaned_text = cleaned_text.replace(",,", " ")
    cleaned_text = cleaned_text.replace("--", " ")

    cleaned_text = re.sub(r"blogs.blackberry.com\S+", " ", cleaned_text)
    cleaned_text = re.sub(r"helpblog.blackberry.com\S+", " ", cleaned_text)

    # Remove repeated letters
    cleaned_text = "".join("".join(s)[:2] for _, s in itertools.groupby(cleaned_text))

    clean_tags = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    cleaned_text = re.sub(clean_tags, " ", cleaned_text)

    clean_urls = re.compile(r"https?://\S+")
    cleaned_text = re.sub(clean_urls, " ", cleaned_text)
    cleaned_text = cleaned_text.replace("=", " ")
    cleaned_text = re.sub(" +", " ", cleaned_text)
    cleaned_text = cleaned_text.strip()
    return cleaned_text


# if not os.path.exists("./reviews_wholeReview.txt"):
    # @Vahid: Could we use the columns:Summary and Voting, somehow?
reviews_for_cellPhones_df = df_review_raw_cellPhones.loc[
    df_review_raw_cellPhones["asin"].isin(Cell_Phones_df.asin.unique())
]
reviews_for_cellPhones_df = reviews_for_cellPhones_df.dropna(
    axis=0, subset=["text"]
)

# Clean reviews and create a text file for all reviews
cellPhone_reviews = reviews_for_cellPhones_df.text
cellPhone_reviews_cleaned = cellPhone_reviews.apply(cleaning_process)

reviews_for_cellPhones_df_cleaned = reviews_for_cellPhones_df.copy()
reviews_for_cellPhones_df_cleaned["text"] = cellPhone_reviews_cleaned.values

wholeReview_reviews_for_cellPhones_df = pd.DataFrame()
wholeReview_reviews_for_cellPhones_df["Index"] = reviews_for_cellPhones_df_cleaned[
    ["asin", "user_id"]
].apply(lambda x: "_".join(x), axis=1)
wholeReview_reviews_for_cellPhones_df["text"] = (
    reviews_for_cellPhones_df_cleaned.text.values
)
wholeReview_reviews_for_cellPhones_df = (
    wholeReview_reviews_for_cellPhones_df.dropna(axis=0, subset=["text"])
)

reviews_for_cellPhones_df_cleaned.to_csv("./reviews_for_cellPhones_df_cleaned.csv")
print("reviews_for_cellPhones_df_cleaned.csv saved")

with open("./reviews_wholeReview.txt", "w") as f:
    for review in cellPhone_reviews_cleaned.values:
        _ = f.write(review + "\n")
# else:
#     print("reviews_wholeReview.txt mil gaya")

brand_list = list(Cell_Phones_df.brand.unique())
print("brand_list: ")
pprint.pprint(brand_list)
os_list = ["ios", "android", "windows", "No"]
memory_list = [
    "2 GB",
    "4 GB",
    "8 GB",
    "16 GB",
    "32 GB",
    "64 GB",
    "128 GB",
    "256 GB",
    "No",
]
color_list = ["White", "Silver", "Black", "Red", "Gold", "No"]

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
    all_combinations_dict[str(i + 1)] = {}
    all_combinations_dict[str(i + 1)]["brand"] = j[0]
    all_combinations_dict[str(i + 1)]["os"] = j[1]
    all_combinations_dict[str(i + 1)]["color"] = j[3]
    all_combinations_dict[str(i + 1)]["memory"] = j[2]


for k, v in list(all_combinations_dict.items())[63:70]:
    print(k, v)

len(all_combinations_dict.keys())

# Generate conversations for the preferences
conversation_dict_part_1 = {}
for k1, v1 in list(all_combinations_dict.items()):
    conversation_dict_part_1["Conv_#" + str(k1)] = {}
    Agent_1 = "Hello, May I help you?"
    User_1 = "Hi, I would like to buy a Cell Phone"
    conversation_dict_part_1[f"Conv_#" + str(k1)]["Agent_1"] = Agent_1
    conversation_dict_part_1["Conv_#" + str(k1)]["User_1"] = User_1
    counter = 1
    for k2, v2 in list(v1.items()):
        counter += 1
        Agent = f"Any preference on {k2}?"
        User = v2
        conversation_dict_part_1["Conv_#" + str(k1)][f"Agent_{counter}"] = Agent
        conversation_dict_part_1["Conv_#" + str(k1)][f"User_{counter}"] = User


for k, v in list(conversation_dict_part_1.items())[50:55]:
    print(k, v)


def findWholeWord(w):
    return re.compile(r"\b({0})\b".format(w), flags=re.IGNORECASE).search


def rules_generator(preferences_dict, features):
    rules = []
    for k2, v2 in list(preferences_dict.items()):
        if k2 != "brand" and v2 != "No":
            rules.append(findWholeWord(str(v2))(features.lower()))
    return rules


retrieved_items_dict = {}
# if not os.path.exists("./retrieved_items_dict.json"):

# Retrieve items for the preferences
DF = Cell_Phones_df
try:
    print("DF")
    pprint.pprint(DF)
except:
    print("Issue found")


for k1, v1 in list(all_combinations_dict.items()):
    list_retrieved_items_final = []
    rules = []
    brand_value = v1["brand"]
    if brand_value == "No":
        df_retrieved_items_brand = DF
    else:
        df_retrieved_items_brand = DF[DF.brand == brand_value]
    zipped = list(
        zip(
            df_retrieved_items_brand.asin.values,
            df_retrieved_items_brand.all_features.values,
        )
    )
    list_retrieved_items_final = []
    for index, features in zipped:
        if features:
            rules = rules_generator(v1, features)
            if all(rules):
                print("Index")
                pprint.pprint(index)
                list_retrieved_items_final.append(index)

    retrieved_items_dict[k1] = {}
    retrieved_items_dict[k1]["preferences"] = v1
    retrieved_items_dict[k1]["retrieved items"] = list_retrieved_items_final


with open("./retrieved_items_dict.json", "w") as f:
    json.dump(retrieved_items_dict, f)
    print("retrieved_items_dict.json saved")
# else:
#     print("mil gaya ./retrieved_items_dict.json")
