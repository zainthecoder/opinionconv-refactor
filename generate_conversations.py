import pandas as pd
import json
import pickle
import re
import random
import numpy as np
import itertools


# Load pickled data instead of JSON files
with open("./100_blocks_neg.pkl", 'rb') as f:
    blocks_neg_100 = pickle.load(f)

with open("./100_blocks_pos.pkl", 'rb') as f:
    blocks_pos_100 = pickle.load(f)


with open("./retrieved_items_dict.json") as f:
    retrieved_items_dict = json.load(f)

metaData_for_cellPhones = pd.read_pickle("./metaData_for_cellPhones.pkl")

all_items_with_review = []
for index in list(retrieved_items_dict.keys()):
    retrieved_items_1 = retrieved_items_dict[str(index)].get("retrieved items")
    retrieved_items_with_review = [
        i
        for i in retrieved_items_1
        if metaData_for_cellPhones.query("asin == @i").num_reviews.values[0] > 0
    ]
    all_items_with_review += retrieved_items_with_review

all_items_with_review = list(set(all_items_with_review))


def find_retrieved_items_and_index(retrieved_items_dict, selected_item):
    all_retrieved_index = []
    all_retrieved_items = []
    for index in range(1, len(retrieved_items_dict.keys()) + 1):
        retrieved_items_list = retrieved_items_dict[str(index)].get("retrieved items")
        if selected_item in retrieved_items_list:
            all_retrieved_index.append(index)
            all_retrieved_items += retrieved_items_dict[str(index)].get(
                "retrieved items"
            )
    all_retrieved_items = list(set(all_retrieved_items))
    return (all_retrieved_index, all_retrieved_items)


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
    return selected_pairs_combination


def conv_type_1(selected_item, num_pairs):
    conv_dict_1 = {}
    tracking_dict = {"Key": [], "Aspect": []}

    all_pairs_list_PP_QA = list(blocks_neg_100[selected_item]["Qpos1A_Apos1A"].keys())
    all_pairs_list_NP_DISAGREEMENT = list(
        blocks_neg_100[selected_item]["Oneg1A_Opos1A"].keys()
    )
    all_pairs_list_PP_QA = list(blocks_neg_100[selected_item]["Qpos1A_Apos1A"].keys())

    all_pairs_combination = list(
        itertools.product(
            all_pairs_list_PP_QA, all_pairs_list_NP_DISAGREEMENT, all_pairs_list_PP_QA
        )
    )
    selected_pairs_combination = select_pairs_combination(
        all_pairs_combination, num_pairs
    )

    for index, selected_pair in enumerate(selected_pairs_combination):
        conv_dict_1["conv_" + str(index + 1)] = {}
        PP_QA = blocks_neg_100[selected_item]["Qpos1A_Apos1A"][selected_pair[0]]
        tracking_dict["Key"].append(PP_QA["Qpos1A"]["Labels"]["Key"])
        tracking_dict["Aspect"].append(PP_QA["Qpos1A"]["Labels"]["Aspect"])
        conv_dict_1["conv_" + str(index + 1)]["pair_1"] = PP_QA

        NP_DISAGREEMENT = blocks_neg_100[selected_item]["Oneg1A_Opos1A"][
            selected_pair[1]
        ]
        if (
            NP_DISAGREEMENT["Oneg1A"]["Labels"]["Key"] not in tracking_dict["Key"]
            and NP_DISAGREEMENT["Opos1A"]["Labels"]["Key"] not in tracking_dict["Key"]
            and NP_DISAGREEMENT["Oneg1A"]["Labels"]["Aspect"]
            not in tracking_dict["Aspect"]
            and NP_DISAGREEMENT["Opos1A"]["Labels"]["Aspect"]
            not in tracking_dict["Aspect"]
        ):
            tracking_dict["Key"].append(NP_DISAGREEMENT["Oneg1A"]["Labels"]["Key"])
            tracking_dict["Key"].append(NP_DISAGREEMENT["Opos1A"]["Labels"]["Key"])
            tracking_dict["Aspect"].append(
                NP_DISAGREEMENT["Oneg1A"]["Labels"]["Aspect"]
            )
            tracking_dict["Aspect"].append(
                NP_DISAGREEMENT["Opos1A"]["Labels"]["Aspect"]
            )
            conv_dict_1["conv_" + str(index + 1)]["pair_2"] = NP_DISAGREEMENT
        else:
            tracking_dict = {"Key": [], "Aspect": []}
            conv_dict_1["conv_" + str(index + 1)] = {}
            continue

        REACTION = "Ah, I see!"
        conv_dict_1["conv_" + str(index + 1)]["pair_3"] = REACTION

        PP_QA = blocks_neg_100[selected_item]["Qpos1A_Apos1A"][selected_pair[2]]
        if (
            PP_QA["Qpos1A"]["Labels"]["Key"] not in tracking_dict["Key"]
            and PP_QA["Qpos1A"]["Labels"]["Aspect"] not in tracking_dict["Aspect"]
        ):

            conv_dict_1["conv_" + str(index + 1)]["pair_4"] = PP_QA
        else:
            tracking_dict = {"Key": [], "Aspect": []}
            conv_dict_1["conv_" + str(index + 1)] = {}
            continue

        DECISION = "Okay! Great! I buy this!"
        conv_dict_1["conv_" + str(index + 1)]["pair_5"] = DECISION
        tracking_dict = {"Key": [], "Aspect": []}

    counter = 0
    conv_dict = {}
    for key in list(conv_dict_1.keys()):
        if conv_dict_1[str(key)]:
            counter += 1
            conv_dict["conv_" + str(counter)] = conv_dict_1[str(key)]
    return conv_dict


selected_item = "B08J4LFDSR"
num_pairs = 20
conv_type_1_test = conv_type_1(selected_item, num_pairs)
print(conv_type_1_test)
