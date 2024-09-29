import pandas as pd
import json
import pickle
import re
import random
import numpy as np

metaData_for_cellPhones = pd.read_pickle(
    "./metaData_for_cellPhones.pkl"
)  # source: MAIN.py
wrong_aspects_3 = pd.read_pickle("./wrong_aspects_3.pkl")

# Path to the input JSON file
input_file = "transformed_data.json"

# Read the JSON file
with open(input_file, "r") as f:
    dict_AspectSentiment = json.load(f)


# add //"B01N6NTIRH", B07D3QKRW1,  B07D3QKRW1, B08FL1N9V3
with open("./sample_retrieved_items_dict.json") as f:  # source: MAIN.py
    retrieved_items_dict = json.load(f)
retrieved_items_dict


wrong_aspects = wrong_aspects_3 + [
    "lumia 1020",
    "zero key",
    "verizon",
    "back",
    "edge",
    "feel",
    "phone",
    "seller",
]

correct_forms = ["bluetooth"]

Q1A_list = [
    "What do you think about its {}?",
    "May I know your opinion on its {}?",
    "What about its {}?",
    "Do you have any views on its {}?",
    "Could you tell me your opinion on its {}?",
    "Do you have any opinions about its {}?",
    "In your honest opinion, how is its {}?",
    "Can you give me your thoughts on its {}?",
    "I’d like to know your views on its {}.",
    "Do you have any particular views on its {}?",
    "From your point of view, how is the {}?",
    "I’d be very interested to know your views on its {}.",
]

Oneg1A_list = [
    "I heard about its {} that ",
    "I was told by one of my friends about its {} that ",
    "As far as I know about its {}, ",
    "What I know about its {} is that ",
]

Opos1A_list = [
    "No, I don't think so, because ",
    "Let me disagree with you, because ",
    "I see your point, but ",
    "I see what you mean, but ",
]

# For MultiWOZ
# Opos1B_list = ["If {} is important for you, we can offer this item. ",
#               "If {} is a crucial feature for you, we have this item. "]

Opos1B_list = [
    "If {} is important for you, we can offer this item: {} ",
    "If {} is a crucial feature for you, we have this item: {} ",
]

Opos2A_list = [
    "I can see what you’re saying but I disagree with you on its {} and even I can tell you something interesting about this phone and its {} that ",
    "I’m sorry but I don’t think so, specially about its {} and I would mention something about the {} of this phone that ",
]

# For MultiWOZ
# Opos1B1_list = ["I heard about this phone and specially its {} that ",
#               "I was told by one of my friends about this phone and its {} that ",
#               "I was wondering if you have this phone, it might be a good choice because as far as I know about its {}, "]

Opos1B1_list = [
    "I heard about this phone {} and specially its {} that ",
    "I was told by one of my friends about this phone {} and its {} that ",
    "I was wondering if you have this phone {}, it might be a good choice because as far as I know about its {}, ",
]

Opos1B2_list = [
    "Yes, it's true! This phone is also a good choice.",
    "Yes, That's so true. This phone is also a good choice.",
    "Yes, That's for sure. This phone is also a good choice.",
    "Yes, I think so too. This phone is also a good choice.",
    "Yes, That is what I think too. This phone is also a good choice.",
    "Yes! I agree with you. This phone is also a good choice.",
    "Yes, I agree with you about it. This phone is also a good choice.",
    "Yes, That's exactly what I know about it. This phone is also a good choice.",
]

Opos2B_list = [
    "Yes, it's true! This phone is also a good choice and even I can tell you something interesting about this phone and its {} that ",
    "Yes, That's so true. This phone is also a good choice and I would mention something about the {} of this phone that ",
    "Yes, That's for sure. This phone is also a good choice and even I can tell you something interesting about this phone and its {} that ",
    "Yes, I think so too. This phone is also a good choice and I would mention something about the {} of this phone that ",
    "Yes, That is what I think too. This phone is also a good choice and even I can tell you something interesting about this phone and its {} that ",
    "Yes! I agree with you. This phone is also a good choice and I would mention something about the {} of this phone that ",
    "Yes, I agree with you about it. This phone is also a good choice and even I can tell you something interesting about this phone and its {} that ",
    "Yes, That's exactly what I know about it. This phone is also a good choice and I would mention something about the {} of this phone that ",
]

Oneg2B_list = [
    "Yes, it's true! This phone might be a good choice but you should know about its {} that ",
    "Yes, That's so true. This phone can be also a good choice but I should say about the {} of this phone that ",
    "Yes, That's for sure. This phone is also a good choice However about the {} of this phone I should say that ",
    "Yes, I completely agree with you. This phone might be a good choice but you should know about its {} that ",
    "Yes, I totally agree with you. This phone can be also a good choice but I should say about the {} of this phone that ",
    "Yes! I agree with you. This phone is also a good choice However about the {} of this phone I should say that ",
    "Yes, I agree with you about it. This phone can be also a good choice but I should say about the {} of this phone that ",
    "Yes, That's exactly what I know about it. However I should say something about the {} of this phone that ",
]


similar_aspect_list = [
    ["android", "android os"],
    ["app", "applications", "apps", "android apps"],
    ["battery", "battery life", "batteries"],
    ["build", "build quality", "built"],
    ["button", "buttons"],
    ["camera", "camera quality"],
    ["charge", "charger", "charges", "charging"],
    ["color", "colors"],
    ["cost", "costs"],
    ["edge", "edges"],
    ["feature", "features"],
    ["front camera", "front facing camera"],
    ["function", "functionality", "functions"],
    ["games", "gaming"],
    ["internal memory", "internal storage"],
    ["keyboard", "keys"],
    ["memory", "memory card"],
    [
        "operating system",
        "os",
    ],
    ["performance", "performs"],
    ["power", "power button"],
    ["price", "price point", "prices"],
    ["screen", "screens"],
    ["micro sd card", "microsd card", "sd card", "microsd slot"],
    ["set up", "setup"],
    ["sim", "sim card"],
    ["sound", "sound quality"],
    ["speaker", "speakerphone", "speakers"],
    ["speed", "speeds"],
    ["touch screen", "touchscreen"],
    ["ui", "user interface"],
]


def aspects_similarity_check(aspect_1, aspect_2, similar_aspect_list):
    check = False
    for i in similar_aspect_list:
        if aspect_1.lower() in i and aspect_2.lower() in i:
            check = True
            break
    if check:
        return True
    else:
        return False


def cleaning_aspect(aspect):
    if aspect != None:
        cleaned_aspect = aspect.replace("/", "")
        cleaned_aspect = re.sub(" +", " ", cleaned_aspect)
        cleaned_aspect = cleaned_aspect.strip()
    else:
        cleaned_aspect = aspect
    return cleaned_aspect


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
    return cleaned_review


def Opos1B_Opos2B(
    item, wrong_aspects, correct_forms, Opos1B_list, Opos2B_list, dict_AspectSentiment
):
    blocks = {}
    counter = 0
    aspect_review_polarity_key_list = []
    item_review_list = dict_AspectSentiment.get(item)

    if item_review_list:
        # Collect all positive reviews for aspects in `aspect_review_polarity_key_list`
        for review_dict in item_review_list:
            for item_reviewer_aspect_key, review_sentiment in review_dict.items():
                key = (
                    review_sentiment["asin"]
                    + "_"
                    + review_sentiment["user_id"]
                    + "_"
                    + item_reviewer_aspect_key
                )
                aspects = review_sentiment.get("aspect", [])  # Handle empty aspect list
                sentiments = review_sentiment.get(
                    "sentiment", []
                )  # Handle empty sentiment list
                review = cleaning_review(review_sentiment["sentence"])

                if aspects:
                    for aspect, polarity in zip(aspects, sentiments):
                        aspect = cleaning_aspect(aspect)
                        if (
                            aspect not in wrong_aspects
                            and aspect is not None
                            and str(polarity).lower() == "positive"
                        ):
                            aspect_review_polarity_key_list.append(
                                (aspect, review, polarity, key)
                            )

    # Process the aspects again and generate positive opinion blocks
    if item_review_list:
        for review_dict in item_review_list:
            for item_reviewer_aspect_key, review_sentiment in review_dict.items():
                key = (
                    review_sentiment["asin"]
                    + "_"
                    + review_sentiment["user_id"]
                    + "_"
                    + item_reviewer_aspect_key
                )
                aspects = review_sentiment.get("aspect", [])  # Handle empty aspect list
                sentiments = review_sentiment.get(
                    "sentiment", []
                )  # Handle empty sentiment list
                review = cleaning_review(review_sentiment["sentence"])

                if aspects:
                    for aspect, polarity in zip(aspects, sentiments):
                        aspect = cleaning_aspect(aspect)
                        if (
                            aspect is not None
                            and aspect not in wrong_aspects
                            and str(polarity).lower() == "positive"
                        ):
                            Opos1B = (
                                random.choice(Opos1B_list).format(item, aspect) + review
                            )

                            # Now generate the Opos2B opinion
                            for (
                                aspect_,
                                review_,
                                polarity_,
                                key_,
                            ) in aspect_review_polarity_key_list:
                                aspect_ = cleaning_aspect(aspect_)
                                if str(polarity_).lower() == "positive" and str(
                                    review
                                ) != str(review_):
                                    counter += 1
                                    Opos2B = (
                                        random.choice(Opos2B_list).format(
                                            aspect, aspect_
                                        )
                                        + review_
                                    )

                                    blocks[f"Opos1B_Opos2B_{counter}"] = {
                                        "Opos1B": {
                                            "Opinion": Opos1B,
                                            "Labels": {
                                                "Key": key,
                                                "Aspect": aspect,
                                                "Polarity": str(polarity).lower(),
                                            },
                                        },
                                        "Opos2B": {
                                            "Opinion": Opos2B,
                                            "Labels": {
                                                "Key": key_,
                                                "Aspect": aspect_,
                                                "Polarity": str(polarity_).lower(),
                                            },
                                        },
                                    }
    return blocks


def Opos1B_Opos1B2(
    item,
    wrong_aspects,
    correct_forms,
    Opos1B1_list,
    Opos1B2_list,
    dict_AspectSentiment,
    only_agreement=True,
    agreement_and_more=True,
):
    blocks = {}
    counter = 0
    similarity = 0
    aspect_review_polarity_key_list = []
    item_review_list = dict_AspectSentiment.get(item)
    if item_review_list and agreement_and_more:
        for review_dict in item_review_list:
            for item_reviewer_aspect_key, review_sentiment in review_dict.items():
                key = (
                    review_sentiment["asin"]
                    + "_"
                    + review_sentiment["user_id"]
                    + "_"
                    + item_reviewer_aspect_key
                )
                aspects = review_sentiment.get("aspect", [])  # Handle empty aspect list
                sentiments = review_sentiment.get(
                    "sentiment", []
                )  # Handle empty sentiment list
                review = cleaning_review(review_sentiment["sentence"])

                if aspects:
                    for aspect, polarity in zip(aspects, sentiments):
                        aspect = cleaning_aspect(aspect)
                        if (
                            aspect not in wrong_aspects
                            and aspect != None
                            and str(polarity).lower() == "positive"
                        ):
                            aspect_review_polarity_key_list.append(
                                (aspect, review, polarity, key)
                            )

    if item_review_list:
        for review_dict in item_review_list:
            for item_reviewer_aspect_key, review_sentiment in review_dict.items():
                key = (
                    review_sentiment["asin"]
                    + "_"
                    + review_sentiment["user_id"]
                    + "_"
                    + item_reviewer_aspect_key
                )
                aspects = review_sentiment.get("aspect", [])  # Handle empty aspect list
                sentiments = review_sentiment.get(
                    "sentiment", []
                )  # Handle empty sentiment list
                review = cleaning_review(review_sentiment["sentence"])

                if aspects:
                    for aspect, polarity in zip(aspects, sentiments):
                        aspect = cleaning_aspect(aspect)
                        if aspect != None and aspect not in wrong_aspects:
                            if str(polarity).lower() == "positive":

                                # For MultiWOZ
                                # Opos1B = random.choice(Opos1B1_list).format(aspect) + sentence_aspect
                                Opos1B = (
                                    random.choice(Opos1B1_list).format(item, aspect)
                                    + review
                                )

                                if only_agreement:
                                    counter += 1

                                    Opos1B2 = random.choice(Opos1B2_list)

                                    blocks["Opos1B_Opos1B2_" + str(counter)] = {}
                                    blocks["Opos1B_Opos1B2_" + str(counter)][
                                        "Opos1B"
                                    ] = {}
                                    blocks["Opos1B_Opos1B2_" + str(counter)]["Opos1B"][
                                        "Opinion"
                                    ] = Opos1B
                                    blocks["Opos1B_Opos1B2_" + str(counter)]["Opos1B"][
                                        "Labels"
                                    ] = {}
                                    blocks["Opos1B_Opos1B2_" + str(counter)]["Opos1B"][
                                        "Labels"
                                    ]["Key"] = key
                                    blocks["Opos1B_Opos1B2_" + str(counter)]["Opos1B"][
                                        "Labels"
                                    ]["Aspect"] = aspect
                                    blocks["Opos1B_Opos1B2_" + str(counter)]["Opos1B"][
                                        "Labels"
                                    ]["Polarity"] = str(polarity).lower()

                                    blocks["Opos1B_Opos1B2_" + str(counter)][
                                        "Opos1B2"
                                    ] = {}
                                    blocks["Opos1B_Opos1B2_" + str(counter)]["Opos1B2"][
                                        "Opinion"
                                    ] = Opos1B2
                                    blocks["Opos1B_Opos1B2_" + str(counter)]["Opos1B2"][
                                        "Labels"
                                    ] = {}
                                    blocks["Opos1B_Opos1B2_" + str(counter)]["Opos1B2"][
                                        "Labels"
                                    ]["Key"] = key
                                    blocks["Opos1B_Opos1B2_" + str(counter)]["Opos1B2"][
                                        "Labels"
                                    ]["Aspect"] = aspect
                                    blocks["Opos1B_Opos1B2_" + str(counter)]["Opos1B2"][
                                        "Labels"
                                    ]["Polarity"] = str(polarity).lower()

                                elif agreement_and_more:

                                    for (
                                        aspect_,
                                        review_,
                                        polarity_,
                                        key_,
                                    ) in aspect_review_polarity_key_list:
                                        aspect_ = cleaning_aspect(aspect_)

                                        if np.logical_or(
                                            aspect == aspect_,
                                            aspects_similarity_check(
                                                aspect, aspect_, similar_aspect_list
                                            ),
                                        ) and str(review_) != str(review):
                                            counter += 1

                                            Opos1B2 = (
                                                random.choice(Opos1B2_list)
                                                + " "
                                                + review_
                                            )

                                            blocks["Opos1B_Opos1B2_" + str(counter)] = (
                                                {}
                                            )
                                            blocks["Opos1B_Opos1B2_" + str(counter)][
                                                "Opos1B"
                                            ] = {}
                                            blocks["Opos1B_Opos1B2_" + str(counter)][
                                                "Opos1B"
                                            ]["Opinion"] = Opos1B
                                            blocks["Opos1B_Opos1B2_" + str(counter)][
                                                "Opos1B"
                                            ]["Labels"] = {}
                                            blocks["Opos1B_Opos1B2_" + str(counter)][
                                                "Opos1B"
                                            ]["Labels"]["Key"] = key
                                            blocks["Opos1B_Opos1B2_" + str(counter)][
                                                "Opos1B"
                                            ]["Labels"]["Aspect"] = aspect
                                            blocks["Opos1B_Opos1B2_" + str(counter)][
                                                "Opos1B"
                                            ]["Labels"]["Polarity"] = str(
                                                polarity
                                            ).lower()

                                            blocks["Opos1B_Opos1B2_" + str(counter)][
                                                "Opos1B2"
                                            ] = {}
                                            blocks["Opos1B_Opos1B2_" + str(counter)][
                                                "Opos1B2"
                                            ]["Opinion"] = Opos1B2
                                            blocks["Opos1B_Opos1B2_" + str(counter)][
                                                "Opos1B2"
                                            ]["Labels"] = {}
                                            blocks["Opos1B_Opos1B2_" + str(counter)][
                                                "Opos1B2"
                                            ]["Labels"]["Key"] = key_
                                            blocks["Opos1B_Opos1B2_" + str(counter)][
                                                "Opos1B2"
                                            ]["Labels"]["Aspect"] = aspect_
                                            blocks["Opos1B_Opos1B2_" + str(counter)][
                                                "Opos1B2"
                                            ]["Labels"]["Polarity"] = str(
                                                polarity_
                                            ).lower()
    return blocks


def Opos1B_Oneg2B(
    item, wrong_aspects, correct_forms, Opos1B1_list, Oneg2B_list, dict_AspectSentiment
):
    blocks = {}
    counter = 0
    similarity = 0
    aspect_review_polarity_key_list = []
    item_review_list = dict_AspectSentiment.get(item)
    if item_review_list:
        for review_dict in item_review_list:
            for item_reviewer_aspect_key, review_sentiment in review_dict.items():
                key = (
                    review_sentiment["asin"]
                    + "_"
                    + review_sentiment["user_id"]
                    + "_"
                    + item_reviewer_aspect_key
                )
                aspects = review_sentiment.get("aspect", [])  # Handle empty aspect list
                sentiments = review_sentiment.get(
                    "sentiment", []
                )  # Handle empty sentiment list
                review = cleaning_review(review_sentiment["sentence"])

                if aspects:
                    for aspect, polarity in zip(aspects, sentiments):
                        aspect = cleaning_aspect(aspect)
                        if aspect not in wrong_aspects and aspect != None:
                            if str(polarity).lower() == "negative":
                                aspect_review_polarity_key_list.append(
                                    (aspect, review, polarity, key)
                                )

    if item_review_list:
        for review_dict in item_review_list:
            for item_reviewer_aspect_key, review_sentiment in review_dict.items():
                kkey = (
                    review_sentiment["asin"]
                    + "_"
                    + review_sentiment["user_id"]
                    + "_"
                    + item_reviewer_aspect_key
                )
                aspects = review_sentiment.get("aspect", [])  # Handle empty aspect list
                sentiments = review_sentiment.get(
                    "sentiment", []
                )  # Handle empty sentiment list
                review = cleaning_review(review_sentiment["sentence"])

                if aspects:
                    for aspect, polarity in zip(aspects, sentiments):
                        aspect = cleaning_aspect(aspect)
                        if aspect != None and aspect not in wrong_aspects:
                            if str(polarity).lower() == "positive":

                                # For MultiWOZ
                                # Opos1B = random.choice(Opos1B1_list).format(aspect) + sentence_aspect
                                Opos1B = (
                                    random.choice(Opos1B1_list).format(item, aspect)
                                    + review
                                )

                                for (
                                    aspect_,
                                    review_,
                                    polarity_,
                                    key_,
                                ) in aspect_review_polarity_key_list:
                                    aspect_ = cleaning_aspect(aspect_)

                                    if str(polarity_).lower() == "negative" and str(
                                        review
                                    ) != str(review_):
                                        counter += 1

                                        Oneg2B = (
                                            random.choice(Oneg2B_list).format(aspect_)
                                            + review_
                                        )

                                        blocks["Opos1B_Oneg2B_" + str(counter)] = {}
                                        blocks["Opos1B_Oneg2B_" + str(counter)][
                                            "Opos1B"
                                        ] = {}
                                        blocks["Opos1B_Oneg2B_" + str(counter)][
                                            "Opos1B"
                                        ]["Opinion"] = Opos1B
                                        blocks["Opos1B_Oneg2B_" + str(counter)][
                                            "Opos1B"
                                        ]["Labels"] = {}
                                        blocks["Opos1B_Oneg2B_" + str(counter)][
                                            "Opos1B"
                                        ]["Labels"]["Key"] = key
                                        blocks["Opos1B_Oneg2B_" + str(counter)][
                                            "Opos1B"
                                        ]["Labels"]["Aspect"] = aspect
                                        blocks["Opos1B_Oneg2B_" + str(counter)][
                                            "Opos1B"
                                        ]["Labels"]["Polarity"] = str(polarity).lower()

                                        blocks["Opos1B_Oneg2B_" + str(counter)][
                                            "Oneg2B"
                                        ] = {}
                                        blocks["Opos1B_Oneg2B_" + str(counter)][
                                            "Oneg2B"
                                        ]["Opinion"] = Oneg2B
                                        blocks["Opos1B_Oneg2B_" + str(counter)][
                                            "Oneg2B"
                                        ]["Labels"] = {}
                                        blocks["Opos1B_Oneg2B_" + str(counter)][
                                            "Oneg2B"
                                        ]["Labels"]["Key"] = key_
                                        blocks["Opos1B_Oneg2B_" + str(counter)][
                                            "Oneg2B"
                                        ]["Labels"]["Aspect"] = aspect_
                                        blocks["Opos1B_Oneg2B_" + str(counter)][
                                            "Oneg2B"
                                        ]["Labels"]["Polarity"] = str(polarity_).lower()
    return blocks


import json
import pickle

save_interval = 10  # Save after every 10 items
counter = 0  # Counter to track how many items have been processed since the last save

save_path_json = "./200_blocks_pos.json"
save_path_pkl = "./done_items_pos.pkl"

# Load previous progress if available
try:
    with open(save_path_pkl, "rb") as fp:
        done_items_pos = pickle.load(fp)
except (FileNotFoundError, EOFError):
    done_items_pos = []

# Start the JSON file if it's the first time writing
try:
    with open(save_path_json, "r") as f:
        # Check if the file has content; continue if it exists
        pass
except (FileNotFoundError, json.JSONDecodeError):
    # If the file doesn't exist, initialize it with an opening curly brace
    with open(save_path_json, "w") as f:
        f.write("{\n")


# Function to append a batch of key-value pairs to the JSON file
def append_to_json_file(file_path, batch_dict):
    with open(file_path, "a") as f:
        for key, value in batch_dict.items():
            # Dump key-value pair and add a comma and newline
            json.dump({key: value}, f)
            f.write(",\n")


for index in list(retrieved_items_dict.keys()):
    print(str(index))
    retrieved_items_1 = retrieved_items_dict[str(index)].get("retrieved items")
    retrieved_items_with_review = [
        i
        for i in retrieved_items_1
        if metaData_for_cellPhones.query("asin == @i").num_reviews.values[0] > 0
    ]
    print("retrieved_items_with_review:", retrieved_items_with_review)
    if len(retrieved_items_with_review) > 0:
        for item in retrieved_items_with_review:
            if item not in done_items_pos:
                print(item)
                item_data = {}
                done_items_pos.append(item)

                blocks_Opos1B_Opos1B2_only_agreement = Opos1B_Opos1B2(
                    item,
                    wrong_aspects,
                    correct_forms,
                    Opos1B1_list,
                    Opos1B2_list,
                    dict_AspectSentiment,
                    only_agreement=True,
                    agreement_and_more=False,
                )
                item_data["Opos1B_Opos1B2_only_agreement"] = (
                    blocks_Opos1B_Opos1B2_only_agreement
                )
                print("Opos1B_Opos1B2_only_agreement is DONE!")

                blocks_Opos1B_Opos1B2_agreement_and_more = Opos1B_Opos1B2(
                    item,
                    wrong_aspects,
                    correct_forms,
                    Opos1B1_list,
                    Opos1B2_list,
                    dict_AspectSentiment,
                    only_agreement=False,
                    agreement_and_more=True,
                )
                item_data["Opos1B_Opos1B2_agreement_and_more"] = (
                    blocks_Opos1B_Opos1B2_agreement_and_more
                )
                print("blocks_Opos1B_Opos1B2_agreement_and_more is DONE!")

                blocks_Opos1B_Opos2B = Opos1B_Opos2B(
                    item,
                    wrong_aspects,
                    correct_forms,
                    Opos1B1_list,
                    Opos2B_list,
                    dict_AspectSentiment,
                )
                item_data["Opos1B_Opos2B"] = blocks_Opos1B_Opos2B
                print("blocks_Opos1B_Opos2B is DONE!")

                blocks_Opos1B_Oneg2B = Opos1B_Oneg2B(
                    item,
                    wrong_aspects,
                    correct_forms,
                    Opos1B1_list,
                    Oneg2B_list,
                    dict_AspectSentiment,
                )
                item_data["Opos1B_Oneg2B"] = blocks_Opos1B_Oneg2B
                print("blocks_Opos1B_Oneg2B is DONE!")

                # Append item data to the JSON file and free memory
                append_to_json_file(save_path_json, {str(item): item_data})
                counter += 1

                # Save progress every 10 items in the pickle file for done_items_neg
                if counter % save_interval == 0:
                    with open(save_path_pkl, "wb") as fp:
                        pickle.dump(done_items_pos, fp, protocol=4)
                    print(f"Progress saved after processing {counter} items.")

                # Free memory after processing each item
                del item_data

# Finalize the JSON by removing the last comma and closing the structure
with open(save_path_json, "rb+") as f:
    f.seek(0, 2)  # Move the pointer to the end of the file
    f.seek(f.tell() - 2, 0)  # Move back two positions to remove the last comma
    f.truncate()  # Remove the last comma
    f.write(b"\n}")  # Close the JSON dictionary

# Final save for done_items_neg
with open(save_path_pkl, "wb") as fp:
    pickle.dump(done_items_pos, fp, protocol=4)

print("Final progress saved!")
