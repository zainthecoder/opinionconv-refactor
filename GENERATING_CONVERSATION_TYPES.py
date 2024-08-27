# # **GENERATING CONVERSATION TYPES:**



# ### Conversation Type #1


# Reaction is separate from other utterences

def conv_type_1(selected_item, num_pairs):
    conv_dict_1 = {}
    tracking_dict = {"Key": [], "Aspect": []}

    all_pairs_list_PP_QA = list(blocks_neg_100[selected_item]['Qpos1A_Apos1A'].keys())
    all_pairs_list_NP_DISAGREEMENT = list(blocks_neg_100[selected_item]['Oneg1A_Opos1A'].keys())
    all_pairs_list_PP_QA = list(blocks_neg_100[selected_item]['Qpos1A_Apos1A'].keys())

    all_pairs_combination = list(itertools.product(all_pairs_list_PP_QA, all_pairs_list_NP_DISAGREEMENT, all_pairs_list_PP_QA))
    selected_pairs_combination = select_pairs_combination(all_pairs_combination, num_pairs)

    for index, selected_pair in enumerate(selected_pairs_combination):
        conv_dict_1['conv_' + str(index + 1)] = {}
        PP_QA = blocks_neg_100[selected_item]['Qpos1A_Apos1A'][selected_pair[0]]
        tracking_dict["Key"].append(PP_QA['Qpos1A']['Labels']['Key'])
        tracking_dict["Aspect"].append(PP_QA['Qpos1A']['Labels']['Aspect'])
        conv_dict_1['conv_' + str(index + 1)]['pair_1'] = PP_QA

        NP_DISAGREEMENT = blocks_neg_100[selected_item]['Oneg1A_Opos1A'][selected_pair[1]]
        if NP_DISAGREEMENT['Oneg1A']['Labels']['Key'] not in tracking_dict["Key"]         and NP_DISAGREEMENT['Opos1A']['Labels']['Key'] not in tracking_dict["Key"]         and NP_DISAGREEMENT['Oneg1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]         and NP_DISAGREEMENT['Opos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
            tracking_dict["Key"].append(NP_DISAGREEMENT['Oneg1A']['Labels']['Key'])
            tracking_dict["Key"].append(NP_DISAGREEMENT['Opos1A']['Labels']['Key'])
            tracking_dict["Aspect"].append(NP_DISAGREEMENT['Oneg1A']['Labels']['Aspect'])
            tracking_dict["Aspect"].append(NP_DISAGREEMENT['Opos1A']['Labels']['Aspect'])
            conv_dict_1['conv_' + str(index + 1)]['pair_2'] = NP_DISAGREEMENT
        else:
            tracking_dict = {"Key": [], "Aspect": []}
            conv_dict_1['conv_' + str(index + 1)] = {}
            continue

        REACTION = "Ah, I see!"
        conv_dict_1['conv_' + str(index + 1)]['pair_3'] = REACTION

        PP_QA = blocks_neg_100[selected_item]['Qpos1A_Apos1A'][selected_pair[2]]
        if PP_QA['Qpos1A']['Labels']['Key'] not in tracking_dict["Key"] and PP_QA['Qpos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
            
            conv_dict_1['conv_' + str(index + 1)]['pair_4'] = PP_QA
        else:
            tracking_dict = {"Key": [], "Aspect": []}
            conv_dict_1['conv_' + str(index + 1)] = {}
            continue

        DECISION = "Okay! Great! I buy this!"
        conv_dict_1['conv_' + str(index + 1)]['pair_5'] = DECISION
        tracking_dict = {"Key": [], "Aspect": []}
    
    counter = 0
    conv_dict = {}
    for key in list(conv_dict_1.keys()):
        if conv_dict_1[str(key)]:
            counter += 1
            conv_dict['conv_' + str(counter)] = conv_dict_1[str(key)]
    return(conv_dict)


selected_item = 'B00AB7FVCY'
num_pairs = 20
conv_type_1_test = conv_type_1(selected_item, num_pairs)
conv_type_1_test['conv_9']


def conv_type_1(selected_item, num_pairs):
    conv_dict_1 = {}
    tracking_dict = {"Key": [], "Aspect": []}

    all_pairs_list_PP_QA = list(blocks_neg_100[selected_item]['Qpos1A_Apos1A'].keys())
    all_pairs_list_NP_DISAGREEMENT = list(blocks_neg_100[selected_item]['Oneg1A_Opos1A'].keys())
    all_pairs_list_PP_QA = list(blocks_neg_100[selected_item]['Qpos1A_Apos1A'].keys())

    all_pairs_combination = list(itertools.product(all_pairs_list_PP_QA, all_pairs_list_NP_DISAGREEMENT, all_pairs_list_PP_QA))
    selected_pairs_combination = select_pairs_combination(all_pairs_combination, num_pairs)

    for index, selected_pair in enumerate(selected_pairs_combination):
        conv_dict_1['conv_' + str(index + 1)] = {}
        PP_QA = blocks_neg_100[selected_item]['Qpos1A_Apos1A'][selected_pair[0]]
        tracking_dict["Key"].append(PP_QA['Qpos1A']['Labels']['Key'])
        tracking_dict["Aspect"].append(PP_QA['Qpos1A']['Labels']['Aspect'])
        conv_dict_1['conv_' + str(index + 1)]['pair_1'] = PP_QA

        NP_DISAGREEMENT = blocks_neg_100[selected_item]['Oneg1A_Opos1A'][selected_pair[1]]
        if NP_DISAGREEMENT['Oneg1A']['Labels']['Key'] not in tracking_dict["Key"]         and NP_DISAGREEMENT['Opos1A']['Labels']['Key'] not in tracking_dict["Key"]         and NP_DISAGREEMENT['Oneg1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]         and NP_DISAGREEMENT['Opos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
            tracking_dict["Key"].append(NP_DISAGREEMENT['Oneg1A']['Labels']['Key'])
            tracking_dict["Key"].append(NP_DISAGREEMENT['Opos1A']['Labels']['Key'])
            tracking_dict["Aspect"].append(NP_DISAGREEMENT['Oneg1A']['Labels']['Aspect'])
            tracking_dict["Aspect"].append(NP_DISAGREEMENT['Opos1A']['Labels']['Aspect'])
            conv_dict_1['conv_' + str(index + 1)]['pair_2'] = NP_DISAGREEMENT
        else:
            tracking_dict = {"Key": [], "Aspect": []}
            conv_dict_1['conv_' + str(index + 1)] = {}
            continue

        PP_QA = blocks_neg_100[selected_item]['Qpos1A_Apos1A'][selected_pair[2]]
        if PP_QA['Qpos1A']['Labels']['Key'] not in tracking_dict["Key"] and PP_QA['Qpos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
            REACTION = "Ah, I see! "
            question_text = REACTION + PP_QA['Qpos1A']['Question']
            new_PP_QA = copy.deepcopy(PP_QA)
            new_PP_QA['Qpos1A']['Question'] = question_text
            conv_dict_1['conv_' + str(index + 1)]['pair_3'] = new_PP_QA
        else:
            tracking_dict = {"Key": [], "Aspect": []}
            conv_dict_1['conv_' + str(index + 1)] = {}
            continue

        DECISION = "Okay! Great! I buy this!"
        conv_dict_1['conv_' + str(index + 1)]['pair_4'] = DECISION
        tracking_dict = {"Key": [], "Aspect": []}
    
    counter = 0
    conv_dict = {}
    for key in list(conv_dict_1.keys()):
        if conv_dict_1[str(key)]:
            counter += 1
            conv_dict['conv_' + str(counter)] = conv_dict_1[str(key)]
    return(conv_dict)


selected_item = 'B00AB7FVCY'
num_pairs = 20
conv_type_1_test = conv_type_1(selected_item, num_pairs)
conv_type_1_test['conv_9']


# ### Conversation Type #2

def conv_type_2(selected_item, num_pairs):
    conv_dict_2 = {}
    tracking_dict = {"Key": [], "Aspect": []}
    all_pairs_list_NP_IT = list(blocks_neg_100[selected_item]['Oneg1A_Opos1B_retrieved'].keys())
    if all_pairs_list_NP_IT:

        all_pairs_list_NP_ATR = list(range(1,num_pairs))

        all_pairs_list_PP_QA = list(range(1,num_pairs))

        all_pairs_combination = list(itertools.product(all_pairs_list_NP_IT, all_pairs_list_NP_ATR, all_pairs_list_PP_QA))
        selected_pairs_combination = select_pairs_combination(all_pairs_combination, num_pairs)

        for index, selected_pair in enumerate(selected_pairs_combination):
            try:
                conv_dict_2['conv_' + str(index + 1)] = {}
                NP_IT = blocks_neg_100[selected_item]['Oneg1A_Opos1B_retrieved'][selected_pair[0]]
                tracking_dict["Key"].append(NP_IT['Oneg1A']['Labels']['Key'])
                tracking_dict["Key"].append(NP_IT['Opos1B']['Labels']['Key'])
                aspect = NP_IT['Opos1B']['Labels']['Aspect']
                selected_item_B = NP_IT['Opos1B']['Labels']['Key'].split("_")[0]
                conv_dict_2['conv_' + str(index + 1)]['pair_1'] = NP_IT

                selected_pair_random = random.choice(list(blocks_neg_100[selected_item_B]['Oneg1A_Opos2A_restricted'].keys()))
                NP_ATR = blocks_neg_100[selected_item_B]['Oneg1A_Opos2A_restricted'][selected_pair_random]
                if NP_ATR['Oneg1A']['Labels']['Key'] not in tracking_dict["Key"]                 and NP_ATR['Opos2A']['Labels']['Key'] not in tracking_dict["Key"]:
                    tracking_dict["Key"].append(NP_ATR['Oneg1A']['Labels']['Key'])
                    tracking_dict["Key"].append(NP_ATR['Opos2A']['Labels']['Key'])
                    tracking_dict["Aspect"].append(NP_ATR['Oneg1A']['Labels']['Aspect'])
                    tracking_dict["Aspect"].append(NP_ATR['Opos2A']['Labels']['Aspect'])
                    
                    REACTION = f"Yes! {aspect} plays a key role for me! "
                    opinion_text = REACTION + NP_ATR['Oneg1A']['Opinion']
                    new_NP_ATR = copy.deepcopy(NP_ATR)
                    new_NP_ATR['Oneg1A']['Opinion'] = opinion_text
                    conv_dict_2['conv_' + str(index + 1)]['pair_2'] = new_NP_ATR
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_2['conv_' + str(index + 1)] = {}
                    continue

                selected_pair_random = random.choice(list(blocks_neg_100[selected_item_B]['Qpos1A_Apos1A'].keys()))
                PP_QA = blocks_neg_100[selected_item_B]['Qpos1A_Apos1A'][selected_pair_random]
                if PP_QA['Qpos1A']['Labels']['Key'] not in tracking_dict["Key"] and PP_QA['Qpos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
                    REACTION = "Ah, Ok! "
                    question_text = REACTION + PP_QA['Qpos1A']['Question']
                    new_PP_QA = copy.deepcopy(PP_QA)
                    new_PP_QA['Qpos1A']['Question'] = question_text
                    conv_dict_2['conv_' + str(index + 1)]['pair_3'] = new_PP_QA
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_2['conv_' + str(index + 1)] = {}
                    continue

                DECISION = "Okay! Great! I buy this!"
                tracking_dict = {"Key": [], "Aspect": []}
                conv_dict_2['conv_' + str(index + 1)]['pair_4'] = DECISION
            except:
                conv_dict_2['conv_' + str(index + 1)] = {}
                tracking_dict = {"Key": [], "Aspect": []}
                continue
    counter = 0
    conv_dict = {}
    for key in list(conv_dict_2.keys()):
        if conv_dict_2[str(key)]:
            counter += 1
            conv_dict['conv_' + str(counter)] = conv_dict_2[str(key)]
    return(conv_dict)


selected_item = 'B00AB7FVCY'
num_pairs = 20
conv_type_2_test = conv_type_2(selected_item, num_pairs)
conv_type_2_test['conv_9']


# ### Conversation Type #3


def conv_type_3(selected_item, num_pairs):
    conv_dict_3 = {}
    tracking_dict = {"Key": [], "Aspect": []}
    all_pairs_list_NP_IT = list(blocks_neg_100[selected_item]['Oneg1A_Opos1B_also_view'].keys())
    if all_pairs_list_NP_IT:

        all_pairs_list_NP_ATR = list(range(1,num_pairs))

        all_pairs_list_PP_QA = list(range(1,num_pairs))

        all_pairs_combination = list(itertools.product(all_pairs_list_NP_IT, all_pairs_list_NP_ATR, all_pairs_list_PP_QA))
        selected_pairs_combination = select_pairs_combination(all_pairs_combination, num_pairs)

        for index, selected_pair in enumerate(selected_pairs_combination):
            try:
                conv_dict_3['conv_' + str(index + 1)] = {}
                NP_IT = blocks_neg_100[selected_item]['Oneg1A_Opos1B_also_view'][selected_pair[0]]
                tracking_dict["Key"].append(NP_IT['Oneg1A']['Labels']['Key'])
                tracking_dict["Key"].append(NP_IT['Opos1B']['Labels']['Key'])
                aspect = NP_IT['Opos1B']['Labels']['Aspect']
                selected_item_B = NP_IT['Opos1B']['Labels']['Key'].split("_")[0]
                conv_dict_3['conv_' + str(index + 1)]['pair_1'] = NP_IT

                selected_pair_random = random.choice(list(blocks_neg_100[selected_item_B]['Oneg1A_Opos2A_restricted'].keys()))
                NP_ATR = blocks_neg_100[selected_item_B]['Oneg1A_Opos2A_restricted'][selected_pair_random]
                if NP_ATR['Oneg1A']['Labels']['Key'] not in tracking_dict["Key"]                 and NP_ATR['Opos2A']['Labels']['Key'] not in tracking_dict["Key"]:
                    tracking_dict["Key"].append(NP_ATR['Oneg1A']['Labels']['Key'])
                    tracking_dict["Key"].append(NP_ATR['Opos2A']['Labels']['Key'])
                    tracking_dict["Aspect"].append(NP_ATR['Oneg1A']['Labels']['Aspect'])
                    tracking_dict["Aspect"].append(NP_ATR['Opos2A']['Labels']['Aspect'])
                    
                    REACTION = f"Yes! {aspect} plays a key role for me! "
                    opinion_text = REACTION + NP_ATR['Oneg1A']['Opinion']
                    new_NP_ATR = copy.deepcopy(NP_ATR)
                    new_NP_ATR['Oneg1A']['Opinion'] = opinion_text
                    conv_dict_3['conv_' + str(index + 1)]['pair_2'] = new_NP_ATR
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_3['conv_' + str(index + 1)] = {}
                    continue

                selected_pair_random = random.choice(list(blocks_neg_100[selected_item_B]['Qpos1A_Apos1A'].keys()))
                PP_QA = blocks_neg_100[selected_item_B]['Qpos1A_Apos1A'][selected_pair_random]
                if PP_QA['Qpos1A']['Labels']['Key'] not in tracking_dict["Key"] and PP_QA['Qpos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
                    REACTION = "Ah, Ok! "
                    question_text = REACTION + PP_QA['Qpos1A']['Question']
                    new_PP_QA = copy.deepcopy(PP_QA)
                    new_PP_QA['Qpos1A']['Question'] = question_text
                    conv_dict_3['conv_' + str(index + 1)]['pair_3'] = new_PP_QA                    
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_3['conv_' + str(index + 1)] = {}
                    continue

                DECISION = "Okay! Great! I buy this!"
                tracking_dict = {"Key": [], "Aspect": []}
                conv_dict_3['conv_' + str(index + 1)]['pair_4'] = DECISION
            except:
                conv_dict_3['conv_' + str(index + 1)] = {}
                tracking_dict = {"Key": [], "Aspect": []}
                continue
    counter = 0
    conv_dict = {}
    for key in list(conv_dict_3.keys()):
        if conv_dict_3[str(key)]:
            counter += 1
            conv_dict['conv_' + str(counter)] = conv_dict_3[str(key)]
    return(conv_dict)


selected_item = 'B00AB7FVCY'
num_pairs = 20
conv_type_3_test = conv_type_3(selected_item, num_pairs)
conv_type_3_test['conv_9']


# ### Conversation Type #4

def conv_type_4(selected_item, num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict):
    conv_dict_4 = {}
    tracking_dict = {"Key": [], "Aspect": []}

    all_pairs_list_NP_DISAGREEMENT = list(blocks_neg_100[selected_item]['Oneg1A_Opos1A'].keys())
    all_pairs_list_PP_QA = list(blocks_neg_100[selected_item]['Qpos1A_Apos1A'].keys())

    if all_pairs_list_NP_DISAGREEMENT and all_pairs_list_PP_QA:
        all_pairs_list_PP_AT = list(range(1,num_pairs))

        all_pairs_combination = list(itertools.product(all_pairs_list_NP_DISAGREEMENT, all_pairs_list_PP_QA, all_pairs_list_PP_AT))
        selected_pairs_combination = select_pairs_combination(all_pairs_combination, num_pairs)

        for index, selected_pair in enumerate(selected_pairs_combination):
            try:
                conv_dict_4['conv_' + str(index + 1)] = {}
                NP_DISAGREEMENT = blocks_neg_100[selected_item]['Oneg1A_Opos1A'][selected_pair[0]]
                tracking_dict["Key"].append(NP_DISAGREEMENT['Oneg1A']['Labels']['Key'])
                tracking_dict["Key"].append(NP_DISAGREEMENT['Opos1A']['Labels']['Key'])
                tracking_dict["Aspect"].append(NP_DISAGREEMENT['Oneg1A']['Labels']['Aspect'])
                tracking_dict["Aspect"].append(NP_DISAGREEMENT['Opos1A']['Labels']['Aspect'])
                conv_dict_4['conv_' + str(index + 1)]['pair_1'] = NP_DISAGREEMENT

                PP_QA = blocks_neg_100[selected_item]['Qpos1A_Apos1A'][selected_pair[1]]
                if PP_QA['Qpos1A']['Labels']['Key'] not in tracking_dict["Key"]                 and PP_QA['Qpos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
                    tracking_dict["Key"].append(PP_QA['Qpos1A']['Labels']['Key'])
                    tracking_dict["Aspect"].append(PP_QA['Qpos1A']['Labels']['Aspect'])
                    
                    REACTION = "All right! "
                    question_text = REACTION + PP_QA['Qpos1A']['Question']
                    new_PP_QA = copy.deepcopy(PP_QA)
                    new_PP_QA['Qpos1A']['Question'] = question_text   
                    conv_dict_4['conv_' + str(index + 1)]['pair_2'] = new_PP_QA
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_4['conv_' + str(index + 1)] = {}
                    continue

                all_also_view_items = metaData_for_cellPhones[metaData_for_cellPhones.asin == selected_item].also_view.values[0]
                all_retrieved_index, all_retrieved_items = find_retrieved_items_and_index(retrieved_items_dict, selected_item)
                all_items_list = list(all_also_view_items) + all_retrieved_items
                all_items_list = list(set(all_items_with_review).intersection(all_items_list))

                selected_item_B = random.choice(all_items_list)

                selected_pair_random = random.choice(list(blocks_pos_100[selected_item_B]['Opos1B_Oneg2B'].keys()))
                PP_AT = blocks_pos_100[selected_item_B]['Opos1B_Oneg2B'][selected_pair_random]
                if PP_AT['Opos1B']['Labels']['Key'] not in tracking_dict["Key"]                 and PP_AT['Oneg2B']['Labels']['Key'] not in tracking_dict["Key"]:
                    conv_dict_4['conv_' + str(index + 1)]['pair_3'] = PP_AT
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_4['conv_' + str(index + 1)] = {}
                    continue

                DECISION = "Ah! Ok! I buy that one!"
                tracking_dict = {"Key": [], "Aspect": []}
                conv_dict_4['conv_' + str(index + 1)]['pair_4'] = DECISION
            except:
                conv_dict_4['conv_' + str(index + 1)] = {}
                tracking_dict = {"Key": [], "Aspect": []}
                continue
    counter = 0
    conv_dict = {}
    for key in list(conv_dict_4.keys()):
        if conv_dict_4[str(key)]:
            counter += 1
            conv_dict['conv_' + str(counter)] = conv_dict_4[str(key)]
    return(conv_dict)


selected_item = 'B00AB7FVCY'
num_pairs = 20
conv_type_4_test = conv_type_4(selected_item, num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict)
conv_type_4_test['conv_9']


# ### Conversation Type #5

def conv_type_5(selected_item, num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict):
    conv_dict_5 = {}
    tracking_dict = {"Key": [], "Aspect": []}

    all_pairs_list_PP_QA = list(blocks_neg_100[selected_item]['Qpos1A_Apos1A'].keys())
    all_pairs_list_NP_DISAGREEMENT = list(blocks_neg_100[selected_item]['Oneg1A_Opos1A'].keys())

    if all_pairs_list_PP_QA and all_pairs_list_NP_DISAGREEMENT:

        all_pairs_list_PN_AT = list(range(1,num_pairs))

        all_pairs_combination = list(itertools.product(all_pairs_list_PP_QA, all_pairs_list_PN_AT, all_pairs_list_NP_DISAGREEMENT))
        selected_pairs_combination = select_pairs_combination(all_pairs_combination, num_pairs)

        for index, selected_pair in enumerate(selected_pairs_combination):
            try:
                conv_dict_5['conv_' + str(index + 1)] = {}
                PP_QA = blocks_neg_100[selected_item]['Qpos1A_Apos1A'][selected_pair[0]]
                tracking_dict["Key"].append(PP_QA['Qpos1A']['Labels']['Key'])
                tracking_dict["Aspect"].append(PP_QA['Qpos1A']['Labels']['Aspect'])
                conv_dict_5['conv_' + str(index + 1)]['pair_1'] = PP_QA

                all_also_view_items = metaData_for_cellPhones[metaData_for_cellPhones.asin == selected_item].also_view.values[0]
                all_retrieved_index, all_retrieved_items = find_retrieved_items_and_index(retrieved_items_dict, selected_item)
                all_items_list = list(all_also_view_items) + all_retrieved_items
                all_items_list = list(set(all_items_with_review).intersection(all_items_list))

                selected_item_B = random.choice(all_items_list)

                selected_pair_random = random.choice(list(blocks_pos_100[selected_item_B]['Opos1B_Oneg2B'].keys()))
                PN_AT = blocks_pos_100[selected_item_B]['Opos1B_Oneg2B'][selected_pair_random]
                if PN_AT['Opos1B']['Labels']['Key'] not in tracking_dict["Key"]                 and PN_AT['Oneg2B']['Labels']['Key'] not in tracking_dict["Key"]:
                    conv_dict_5['conv_' + str(index + 1)]['pair_2'] = PN_AT
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_5['conv_' + str(index + 1)] = {}
                    continue

                NP_DISAGREEMENT = blocks_neg_100[selected_item]['Oneg1A_Opos1A'][selected_pair[2]]
                if NP_DISAGREEMENT['Oneg1A']['Labels']['Key'] not in tracking_dict["Key"]                 and NP_DISAGREEMENT['Opos1A']['Labels']['Key'] not in tracking_dict["Key"]                 and NP_DISAGREEMENT['Oneg1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]                 and NP_DISAGREEMENT['Opos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
                    REACTION = "Ah, Ok! "
                    opinion_text = REACTION + NP_DISAGREEMENT['Oneg1A']['Opinion']
                    new_NP_DISAGREEMENT = copy.deepcopy(NP_DISAGREEMENT)
                    new_NP_DISAGREEMENT['Oneg1A']['Opinion'] = opinion_text
                    conv_dict_5['conv_' + str(index + 1)]['pair_3'] = new_NP_DISAGREEMENT                    
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_5['conv_' + str(index + 1)] = {}
                    continue

                DECISION = "Ok!, Great! So, I buy this!"
                tracking_dict = {"Key": [], "Aspect": []}
                conv_dict_5['conv_' + str(index + 1)]['pair_4'] = DECISION
            except:
                conv_dict_5['conv_' + str(index + 1)] = {}
                tracking_dict = {"Key": [], "Aspect": []}
                continue
    counter = 0
    conv_dict = {}
    for key in list(conv_dict_5.keys()):
        if conv_dict_5[str(key)]:
            counter += 1
            conv_dict['conv_' + str(counter)] = conv_dict_5[str(key)]
    return(conv_dict)


selected_item = 'B00AB7FVCY'
num_pairs = 20
conv_type_5_test = conv_type_5(selected_item, num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict)
conv_type_5_test['conv_9']


# ### Conversation Type #6

def conv_type_6(selected_item, num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict):
    conv_dict_6 = {}
    tracking_dict = {"Key": [], "Aspect": []}

    all_pairs_list_NP_ATR = list(blocks_neg_100[selected_item]['Oneg1A_Opos2A_restricted'].keys())
    all_pairs_list_PP_QA = list(blocks_neg_100[selected_item]['Qpos1A_Apos1A'].keys())

    if all_pairs_list_NP_ATR and all_pairs_list_PP_QA:
        all_pairs_list_PP_AGREEMENT_M = list(range(1,num_pairs))

        all_pairs_combination = list(itertools.product(all_pairs_list_NP_ATR, all_pairs_list_PP_QA, all_pairs_list_PP_AGREEMENT_M))
        selected_pairs_combination = select_pairs_combination(all_pairs_combination, num_pairs)

        for index, selected_pair in enumerate(selected_pairs_combination):
            try:
                conv_dict_6['conv_' + str(index + 1)] = {}
                NP_ATR = blocks_neg_100[selected_item]['Oneg1A_Opos2A_restricted'][selected_pair[0]]
                tracking_dict["Key"].append(NP_ATR['Oneg1A']['Labels']['Key'])
                tracking_dict["Key"].append(NP_ATR['Opos2A']['Labels']['Key'])
                tracking_dict["Aspect"].append(NP_ATR['Oneg1A']['Labels']['Aspect'])
                tracking_dict["Aspect"].append(NP_ATR['Opos2A']['Labels']['Aspect'])
                conv_dict_6['conv_' + str(index + 1)]['pair_1'] = NP_ATR

                PP_QA = blocks_neg_100[selected_item]['Qpos1A_Apos1A'][selected_pair[1]]
                if PP_QA['Qpos1A']['Labels']['Key'] not in tracking_dict["Key"]                 and PP_QA['Qpos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
                    conv_dict_6['conv_' + str(index + 1)]['pair_2'] = PP_QA
                    #Because we change the product
                    tracking_dict = {"Key": [], "Aspect": []}
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_6['conv_' + str(index + 1)] = {}
                    continue

                all_also_view_items = metaData_for_cellPhones[metaData_for_cellPhones.asin == selected_item].also_view.values[0]
                all_retrieved_index, all_retrieved_items = find_retrieved_items_and_index(retrieved_items_dict, selected_item)
                all_items_list = list(all_also_view_items) + all_retrieved_items
                all_items_list = list(set(all_items_with_review).intersection(all_items_list))

                selected_item_B = random.choice(all_items_list)

                selected_pair_random = random.choice(list(blocks_pos_100[selected_item_B]['Opos1B_Opos1B2_agreement_and_more'].keys()))
                PP_AGREEMENT_M = blocks_pos_100[selected_item_B]['Opos1B_Opos1B2_agreement_and_more'][selected_pair_random]
                tracking_dict["Key"].append(PP_AGREEMENT_M['Opos1B']['Labels']['Key'])
                tracking_dict["Key"].append(PP_AGREEMENT_M['Opos1B2']['Labels']['Key'])
                tracking_dict["Aspect"].append(PP_AGREEMENT_M['Opos1B']['Labels']['Aspect'])
                tracking_dict["Aspect"].append(PP_AGREEMENT_M['Opos1B2']['Labels']['Aspect'])
                conv_dict_6['conv_' + str(index + 1)]['pair_3'] = PP_AGREEMENT_M

                selected_pair_random = random.choice(list(blocks_neg_100[selected_item_B]['Qpos1A_Apos1A'].keys()))
                PP_QA = blocks_neg_100[selected_item_B]['Qpos1A_Apos1A'][selected_pair_random]
                if PP_QA['Qpos1A']['Labels']['Key'] not in tracking_dict["Key"]                 and PP_QA['Qpos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
                    conv_dict_6['conv_' + str(index + 1)]['pair_4'] = PP_QA
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_6['conv_' + str(index + 1)] = {}
                    continue

                DECISION = "Ok!, Great! I buy this!"
                tracking_dict = {"Key": [], "Aspect": []}
                conv_dict_6['conv_' + str(index + 1)]['pair_5'] = DECISION
            except:
                conv_dict_6['conv_' + str(index + 1)] = {}
                tracking_dict = {"Key": [], "Aspect": []}
                continue
    counter = 0
    conv_dict = {}
    for key in list(conv_dict_6.keys()):
        if conv_dict_6[str(key)]:
            counter += 1
            conv_dict['conv_' + str(counter)] = conv_dict_6[str(key)]
    return(conv_dict)


selected_item = 'B00AB7FVCY'
num_pairs = 20
conv_type_6_test = conv_type_6(selected_item, num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict)
conv_type_6_test['conv_9']


# ### Conversation Type #7


def conv_type_7(selected_item, num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict):
    conv_dict_7 = {}
    tracking_dict = {"Key": [], "Aspect": []}

    all_pairs_list_NP_ATR = list(blocks_neg_100[selected_item]['Oneg1A_Opos2A_restricted'].keys())
    all_pairs_list_PP_QA = list(blocks_neg_100[selected_item]['Qpos1A_Apos1A'].keys())

    if all_pairs_list_NP_ATR and all_pairs_list_PP_QA:
        all_pairs_list_PP_AT = list(range(1,num_pairs))

        all_pairs_combination = list(itertools.product(all_pairs_list_NP_ATR, all_pairs_list_PP_QA, all_pairs_list_PP_AT))
        selected_pairs_combination = select_pairs_combination(all_pairs_combination, num_pairs)

        for index, selected_pair in enumerate(selected_pairs_combination):
            try:
                conv_dict_7['conv_' + str(index + 1)] = {}
                NP_ATR = blocks_neg_100[selected_item]['Oneg1A_Opos2A_restricted'][selected_pair[0]]
                tracking_dict["Key"].append(NP_ATR['Oneg1A']['Labels']['Key'])
                tracking_dict["Key"].append(NP_ATR['Opos2A']['Labels']['Key'])
                tracking_dict["Aspect"].append(NP_ATR['Oneg1A']['Labels']['Aspect'])
                tracking_dict["Aspect"].append(NP_ATR['Opos2A']['Labels']['Aspect'])
                conv_dict_7['conv_' + str(index + 1)]['pair_1'] = NP_ATR

                PP_QA = blocks_neg_100[selected_item]['Qpos1A_Apos1A'][selected_pair[1]]
                if PP_QA['Qpos1A']['Labels']['Key'] not in tracking_dict["Key"]                 and PP_QA['Qpos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
                    conv_dict_7['conv_' + str(index + 1)]['pair_2'] = PP_QA
                    #Because we change the product
                    tracking_dict = {"Key": [], "Aspect": []}
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_7['conv_' + str(index + 1)] = {}
                    continue

                all_also_view_items = metaData_for_cellPhones[metaData_for_cellPhones.asin == selected_item].also_view.values[0]
                all_retrieved_index, all_retrieved_items = find_retrieved_items_and_index(retrieved_items_dict, selected_item)
                all_items_list = list(all_also_view_items) + all_retrieved_items
                all_items_list = list(set(all_items_with_review).intersection(all_items_list))

                selected_item_B = random.choice(all_items_list)

                selected_pair_random = random.choice(list(blocks_pos_100[selected_item_B]['Opos1B_Opos2B'].keys()))
                PP_AT = blocks_pos_100[selected_item_B]['Opos1B_Opos2B'][selected_pair_random]
                tracking_dict["Key"].append(PP_AT['Opos1B']['Labels']['Key'])
                tracking_dict["Key"].append(PP_AT['Opos2B']['Labels']['Key'])
                tracking_dict["Aspect"].append(PP_AT['Opos1B']['Labels']['Aspect'])
                tracking_dict["Aspect"].append(PP_AT['Opos2B']['Labels']['Aspect'])
                conv_dict_7['conv_' + str(index + 1)]['pair_3'] = PP_AT

                selected_pair_random = random.choice(list(blocks_neg_100[selected_item_B]['Qpos1A_Apos1A'].keys()))
                PP_QA = blocks_neg_100[selected_item_B]['Qpos1A_Apos1A'][selected_pair_random]
                if PP_QA['Qpos1A']['Labels']['Key'] not in tracking_dict["Key"]                 and PP_QA['Qpos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
                    conv_dict_7['conv_' + str(index + 1)]['pair_4'] = PP_QA
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_7['conv_' + str(index + 1)] = {}
                    continue

                DECISION = "Ok!, Great! I buy this!"
                tracking_dict = {"Key": [], "Aspect": []}
                conv_dict_7['conv_' + str(index + 1)]['pair_5'] = DECISION
            except:
                conv_dict_7['conv_' + str(index + 1)] = {}
                tracking_dict = {"Key": [], "Aspect": []}
                continue
    counter = 0
    conv_dict = {}
    for key in list(conv_dict_7.keys()):
        if conv_dict_7[str(key)]:
            counter += 1
            conv_dict['conv_' + str(counter)] = conv_dict_7[str(key)]
    return(conv_dict)


selected_item = 'B00AB7FVCY'
num_pairs = 20
conv_type_7_test = conv_type_7(selected_item, num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict)
conv_type_7_test['conv_1']


# ### Conversation Type #8

def conv_type_8(selected_item, num_pairs):
    conv_dict_8 = {}
    tracking_dict = {"Key": [], "Aspect": []}

    all_pairs_list_PP_QA_1 = list(blocks_neg_100[selected_item]['Qpos1A_Apos1A'].keys())
    all_pairs_list_NP_IT = list(blocks_neg_100[selected_item]['Oneg1A_Opos1B_retrieved'].keys())

    if all_pairs_list_PP_QA_1 and all_pairs_list_NP_IT:
        all_pairs_list_PP_QA_2 = list(range(1,num_pairs))

        all_pairs_combination = list(itertools.product(all_pairs_list_PP_QA_1, all_pairs_list_NP_IT, all_pairs_list_PP_QA_2))
        selected_pairs_combination = select_pairs_combination(all_pairs_combination, num_pairs)

        for index, selected_pair in enumerate(selected_pairs_combination):
            try:
                conv_dict_8['conv_' + str(index + 1)] = {}
                PP_QA = blocks_neg_100[selected_item]['Qpos1A_Apos1A'][selected_pair[0]]
                tracking_dict["Key"].append(PP_QA['Qpos1A']['Labels']['Key'])
                tracking_dict["Aspect"].append(PP_QA['Qpos1A']['Labels']['Aspect'])
                conv_dict_8['conv_' + str(index + 1)]['pair_1'] = PP_QA

                NP_IT = blocks_neg_100[selected_item]['Oneg1A_Opos1B_retrieved'][selected_pair[1]]
                if NP_IT['Oneg1A']['Labels']['Key'] not in tracking_dict["Key"]                 and NP_IT['Opos1B']['Labels']['Key'] not in tracking_dict["Key"]:
                    aspect = NP_IT['Opos1B']['Labels']['Aspect']
                    selected_item_B = NP_IT['Opos1B']['Labels']['Key'].split("_")[0]
                    REACTION = "But "
                    opinion_text = REACTION + NP_IT['Oneg1A']['Opinion']
                    new_NP_IT = copy.deepcopy(NP_IT)
                    new_NP_IT['Oneg1A']['Opinion'] = opinion_text
                    conv_dict_8['conv_' + str(index + 1)]['pair_2'] = new_NP_IT                    
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_8['conv_' + str(index + 1)] = {}
                    continue

                selected_pair_random = random.choice(list(blocks_neg_100[selected_item_B]['Qpos1A_Apos1A'].keys()))
                PP_QA = blocks_neg_100[selected_item_B]['Qpos1A_Apos1A'][selected_pair_random]
                conv_dict_8['conv_' + str(index + 1)]['pair_3'] = PP_QA

                DECISION = "Okay! Great! I buy this!"
                tracking_dict = {"Key": [], "Aspect": []}
                conv_dict_8['conv_' + str(index + 1)]['pair_4'] = DECISION
            except:
                conv_dict_8['conv_' + str(index + 1)] = {}
                tracking_dict = {"Key": [], "Aspect": []}
                continue
    counter = 0
    conv_dict = {}
    for key in list(conv_dict_8.keys()):
        if conv_dict_8[str(key)]:
            counter += 1
            conv_dict['conv_' + str(counter)] = conv_dict_8[str(key)]
    return(conv_dict)


selected_item = 'B00AB7FVCY'
num_pairs = 20
conv_type_8_test = conv_type_8(selected_item, num_pairs)
conv_type_8_test['conv_9']

# ### Conversation Type #9

def conv_type_9(selected_item, num_pairs):
    conv_dict_9 = {}
    tracking_dict = {"Key": [], "Aspect": []}

    all_pairs_list_PP_AGREEMENT_M = list(blocks_pos_100[selected_item]['Opos1B_Opos1B2_agreement_and_more'].keys())
    all_pairs_list_PP_QA = list(blocks_neg_100[selected_item]['Qpos1A_Apos1A'].keys())

    all_pairs_combination = list(itertools.product(all_pairs_list_PP_AGREEMENT_M, all_pairs_list_PP_QA))
    selected_pairs_combination = select_pairs_combination(all_pairs_combination, num_pairs)

    for index, selected_pair in enumerate(selected_pairs_combination):
        conv_dict_9['conv_' + str(index + 1)] = {}
        PP_AGREEMENT_M = blocks_pos_100[selected_item]['Opos1B_Opos1B2_agreement_and_more'][selected_pair[0]]
        tracking_dict["Key"].append(PP_AGREEMENT_M['Opos1B']['Labels']['Key'])
        tracking_dict["Key"].append(PP_AGREEMENT_M['Opos1B2']['Labels']['Key'])
        tracking_dict["Aspect"].append(PP_AGREEMENT_M['Opos1B']['Labels']['Aspect'])
        tracking_dict["Aspect"].append(PP_AGREEMENT_M['Opos1B2']['Labels']['Aspect'])
        conv_dict_9['conv_' + str(index + 1)]['pair_1'] = PP_AGREEMENT_M

        PP_QA = blocks_neg_100[selected_item]['Qpos1A_Apos1A'][selected_pair[1]]
        if PP_QA['Qpos1A']['Labels']['Key'] not in tracking_dict["Key"]         and PP_QA['Qpos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
            REACTION = "Ok! Great! "
            question_text = REACTION + PP_QA['Qpos1A']['Question']
            new_PP_QA = copy.deepcopy(PP_QA)
            new_PP_QA['Qpos1A']['Question'] = question_text   
            conv_dict_9['conv_' + str(index + 1)]['pair_2'] = new_PP_QA
        else:
            tracking_dict = {"Key": [], "Aspect": []}
            conv_dict_9['conv_' + str(index + 1)] = {}
            continue

        DECISION = "Okay! I buy this!"
        tracking_dict = {"Key": [], "Aspect": []}
        conv_dict_9['conv_' + str(index + 1)]['pair_3'] = DECISION
    counter = 0
    conv_dict = {}
    for key in list(conv_dict_9.keys()):
        if conv_dict_9[str(key)]:
            counter += 1
            conv_dict['conv_' + str(counter)] = conv_dict_9[str(key)]
    return(conv_dict)


selected_item = 'B00AB7FVCY'
num_pairs = 20
conv_type_9_test = conv_type_9(selected_item, num_pairs)
conv_type_9_test['conv_9']


# ### Conversation Type #10

def conv_type_10(selected_item, num_pairs):
    conv_dict_10 = {}
    tracking_dict = {"Key": [], "Aspect": []}

    all_pairs_list_PP_AT = list(blocks_pos_100[selected_item]['Opos1B_Opos2B'].keys())
    all_pairs_list_PP_QA = list(blocks_neg_100[selected_item]['Qpos1A_Apos1A'].keys())

    all_pairs_combination = list(itertools.product(all_pairs_list_PP_AT, all_pairs_list_PP_QA))
    selected_pairs_combination = select_pairs_combination(all_pairs_combination, num_pairs)

    for index, selected_pair in enumerate(selected_pairs_combination):
        conv_dict_10['conv_' + str(index + 1)] = {}
        PP_AT = blocks_pos_100[selected_item]['Opos1B_Opos2B'][selected_pair[0]]
        tracking_dict["Key"].append(PP_AT['Opos1B']['Labels']['Key'])
        tracking_dict["Key"].append(PP_AT['Opos2B']['Labels']['Key'])
        tracking_dict["Aspect"].append(PP_AT['Opos1B']['Labels']['Aspect'])
        tracking_dict["Aspect"].append(PP_AT['Opos2B']['Labels']['Aspect'])
        conv_dict_10['conv_' + str(index + 1)]['pair_1'] = PP_AT

        PP_QA = blocks_neg_100[selected_item]['Qpos1A_Apos1A'][selected_pair[1]]
        if PP_QA['Qpos1A']['Labels']['Key'] not in tracking_dict["Key"]         and PP_QA['Qpos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
            REACTION = "Ok! Great! "
            question_text = REACTION + PP_QA['Qpos1A']['Question']
            new_PP_QA = copy.deepcopy(PP_QA)
            new_PP_QA['Qpos1A']['Question'] = question_text   
            conv_dict_10['conv_' + str(index + 1)]['pair_2'] = new_PP_QA
        else:
            tracking_dict = {"Key": [], "Aspect": []}
            conv_dict_10['conv_' + str(index + 1)] = {}
            continue

        DECISION = "Okay! I buy this!"
        tracking_dict = {"Key": [], "Aspect": []}
        conv_dict_10['conv_' + str(index + 1)]['pair_3'] = DECISION
    
    counter = 0
    conv_dict = {}
    for key in list(conv_dict_10.keys()):
        if conv_dict_10[str(key)]:
            counter += 1
            conv_dict['conv_' + str(counter)] = conv_dict_10[str(key)]
    return(conv_dict)


selected_item = 'B00AB7FVCY'
num_pairs = 20
conv_type_10_test = conv_type_10(selected_item, num_pairs)
conv_type_10_test['conv_9']

# ### Conversation Type #11

def conv_type_11(selected_item, num_pairs):
    conv_dict_11 = {}
    tracking_dict = {"Key": [], "Aspect": []}

    all_pairs_list_PN_AT = list(blocks_pos_100[selected_item]['Opos1B_Oneg2B'].keys())
    all_pairs_list_PP_QA = list(blocks_neg_100[selected_item]['Qpos1A_Apos1A'].keys())

    all_pairs_combination = list(itertools.product(all_pairs_list_PN_AT, all_pairs_list_PP_QA))
    selected_pairs_combination = select_pairs_combination(all_pairs_combination, num_pairs)

    for index, selected_pair in enumerate(selected_pairs_combination):
        conv_dict_11['conv_' + str(index + 1)] = {}
        PN_AT = blocks_pos_100[selected_item]['Opos1B_Oneg2B'][selected_pair[0]]
        tracking_dict["Key"].append(PN_AT['Opos1B']['Labels']['Key'])
        tracking_dict["Key"].append(PN_AT['Oneg2B']['Labels']['Key'])
        tracking_dict["Aspect"].append(PN_AT['Opos1B']['Labels']['Aspect'])
        tracking_dict["Aspect"].append(PN_AT['Oneg2B']['Labels']['Aspect'])
        aspect = PN_AT['Oneg2B']['Labels']['Aspect']
        conv_dict_11['conv_' + str(index + 1)]['pair_1'] = PN_AT

        PP_QA = blocks_neg_100[selected_item]['Qpos1A_Apos1A'][selected_pair[1]]
        if PP_QA['Qpos1A']['Labels']['Key'] not in tracking_dict["Key"]         and PP_QA['Qpos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
            REACTION = f"But {aspect} doesn't play a key role for me! "
            question_text = REACTION + PP_QA['Qpos1A']['Question']
            new_PP_QA = copy.deepcopy(PP_QA)
            new_PP_QA['Qpos1A']['Question'] = question_text   
            conv_dict_11['conv_' + str(index + 1)]['pair_2'] = new_PP_QA
        else:
            tracking_dict = {"Key": [], "Aspect": []}
            conv_dict_11['conv_' + str(index + 1)] = {}
            continue

        DECISION = "Okay! I buy this!"
        tracking_dict = {"Key": [], "Aspect": []}
        conv_dict_11['conv_' + str(index + 1)]['pair_3'] = DECISION
    
    counter = 0
    conv_dict = {}
    for key in list(conv_dict_11.keys()):
        if conv_dict_11[str(key)]:
            counter += 1
            conv_dict['conv_' + str(counter)] = conv_dict_11[str(key)]
    return(conv_dict)


selected_item = 'B00AB7FVCY'
num_pairs = 20
conv_type_11_test = conv_type_11(selected_item, num_pairs)
conv_type_11_test['conv_9']


# ### Conversation Type #12

def conv_type_12(selected_item, num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict):
    conv_dict_12 = {}
    tracking_dict = {"Key": [], "Aspect": []}

    all_pairs_list_PN_AT = list(blocks_pos_100[selected_item]['Opos1B_Oneg2B'].keys())

    if all_pairs_list_PN_AT:
        all_pairs_list_PP_QA = list(range(1, num_pairs))

        all_pairs_combination = list(itertools.product(all_pairs_list_PN_AT, all_pairs_list_PP_QA))
        selected_pairs_combination = select_pairs_combination(all_pairs_combination, num_pairs)

        for index, selected_pair in enumerate(selected_pairs_combination):
            try:
                conv_dict_12['conv_' + str(index + 1)] = {}
                PN_AT = blocks_pos_100[selected_item]['Opos1B_Oneg2B'][selected_pair[0]]
                tracking_dict["Key"].append(PN_AT['Opos1B']['Labels']['Key'])
                tracking_dict["Key"].append(PN_AT['Oneg2B']['Labels']['Key'])
                tracking_dict["Aspect"].append(PN_AT['Oneg2B']['Labels']['Aspect'])
                aspect = PN_AT['Oneg2B']['Labels']['Aspect']
                conv_dict_12['conv_' + str(index + 1)]['pair_1'] = PN_AT

                all_also_view_items = metaData_for_cellPhones[metaData_for_cellPhones.asin == selected_item].also_view.values[0]
                all_retrieved_index, all_retrieved_items = find_retrieved_items_and_index(retrieved_items_dict, selected_item)
                all_items_list = list(all_also_view_items) + all_retrieved_items
                all_items_list = list(set(all_items_with_review).intersection(all_items_list))

                selected_item_B = random.choice(all_items_list)
                
                REACTION = {"Reaction_user": f"Ah! {aspect} plays a key role for me!",
                            "Reaction_agent": f"Okay! So, I can offer you this one: {selected_item_B}"}
                conv_dict_12['conv_' + str(index + 1)]['pair_2'] = REACTION

                #REACTION = {"Reaction_user": f"Ah! {aspect} plays a key role for me!",
                            #"Reaction_agent": f"Okay! So, I can offer you this one: {selected_item_B}"}
                #conv_dict_12['conv_' + str(index + 1)]['pair_2'] = REACTION

                selected_pair_random = random.choice(list(blocks_neg_100[selected_item_B]['Qpos1A_Apos1A'].keys()))
                PP_QA = blocks_neg_100[selected_item_B]['Qpos1A_Apos1A'][selected_pair_random]
                if PP_QA['Qpos1A']['Labels']['Key'] not in tracking_dict["Key"]                 and PP_QA['Qpos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
                    conv_dict_12['conv_' + str(index + 1)]['pair_3'] = PP_QA
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_12['conv_' + str(index + 1)] = {}
                    continue

                DECISION = "Ok!, I buy this!"
                tracking_dict = {"Key": [], "Aspect": []}
                conv_dict_12['conv_' + str(index + 1)]['pair_4'] = DECISION
            except:
                conv_dict_12['conv_' + str(index + 1)] = {}
                tracking_dict = {"Key": [], "Aspect": []}
                continue
    counter = 0
    conv_dict = {}
    for key in list(conv_dict_12.keys()):
        if conv_dict_12[str(key)]:
            counter += 1
            conv_dict['conv_' + str(counter)] = conv_dict_12[str(key)]
    return(conv_dict)


selected_item = 'B00AB7FVCY'
num_pairs = 20
conv_type_12_test = conv_type_12(selected_item, num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict)
conv_type_12_test['conv_9']


# ### Conversation Type #13

def conv_type_13(selected_item, num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict):
    conv_dict_13 = {}
    tracking_dict = {"Key": [], "Aspect": []}

    all_pairs_list_PP_QA_1 = list(blocks_neg_100[selected_item]['Qpos1A_Apos1A'].keys())
    all_pairs_list_NP_ATR = list(blocks_neg_100[selected_item]['Oneg1A_Opos2A_restricted'].keys())
    all_pairs_list_PP_QA_2 = list(blocks_neg_100[selected_item]['Qpos1A_Apos1A'].keys())

    if all_pairs_list_PP_QA_1 and all_pairs_list_NP_ATR:
        all_pairs_list_PN_AT = list(range(1, num_pairs))

        all_pairs_combination = list(itertools.product(all_pairs_list_PP_QA_1, all_pairs_list_NP_ATR, all_pairs_list_PN_AT, all_pairs_list_PP_QA_2))
        selected_pairs_combination = select_pairs_combination(all_pairs_combination, num_pairs)

        for index, selected_pair in enumerate(selected_pairs_combination):
            try:
                conv_dict_13['conv_' + str(index + 1)] = {}
                PP_QA = blocks_neg_100[selected_item]['Qpos1A_Apos1A'][selected_pair[0]]
                tracking_dict["Key"].append(PP_QA['Qpos1A']['Labels']['Key'])
                tracking_dict["Aspect"].append(PP_QA['Qpos1A']['Labels']['Aspect'])
                conv_dict_13['conv_' + str(index + 1)]['pair_1'] = PP_QA

                NP_ATR = blocks_neg_100[selected_item]['Oneg1A_Opos2A_restricted'][selected_pair[1]]
                if NP_ATR['Opos2A']['Labels']['Key'] not in tracking_dict["Key"]:
                    tracking_dict["Key"].append(NP_ATR['Oneg1A']['Labels']['Key'])
                    tracking_dict["Key"].append(NP_ATR['Opos2A']['Labels']['Key'])
                    tracking_dict["Aspect"].append(NP_ATR['Oneg1A']['Labels']['Aspect'])
                    tracking_dict["Aspect"].append(NP_ATR['Opos2A']['Labels']['Aspect'])
                    conv_dict_13['conv_' + str(index + 1)]['pair_2'] = NP_ATR
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_13['conv_' + str(index + 1)] = {}
                    continue


                all_also_view_items = metaData_for_cellPhones[metaData_for_cellPhones.asin == selected_item].also_view.values[0]
                all_retrieved_index, all_retrieved_items = find_retrieved_items_and_index(retrieved_items_dict, selected_item)
                all_items_list = list(all_also_view_items) + all_retrieved_items
                all_items_list = list(set(all_items_with_review).intersection(all_items_list))

                selected_item_B = random.choice(all_items_list)

                selected_pair_random = random.choice(list(blocks_pos_100[selected_item_B]['Opos1B_Oneg2B'].keys()))
                PN_AT = blocks_pos_100[selected_item_B]['Opos1B_Oneg2B'][selected_pair_random]
                if PN_AT['Opos1B']['Labels']['Key'] not in tracking_dict["Key"]                 and PN_AT['Oneg2B']['Labels']['Key'] not in tracking_dict["Key"]:
                    conv_dict_13['conv_' + str(index + 1)]['pair_3'] = PN_AT
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_13['conv_' + str(index + 1)] = {}
                    continue

                PP_QA = blocks_neg_100[selected_item]['Qpos1A_Apos1A'][selected_pair[3]]
                if PP_QA['Qpos1A']['Labels']['Key'] not in tracking_dict["Key"]                 and PP_QA['Qpos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
                    REACTION = "Ah! Ok! "
                    question_text = REACTION + PP_QA['Qpos1A']['Question']
                    new_PP_QA = copy.deepcopy(PP_QA)
                    new_PP_QA['Qpos1A']['Question'] = question_text   
                    conv_dict_13['conv_' + str(index + 1)]['pair_4'] = new_PP_QA
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_13['conv_' + str(index + 1)] = {}
                    continue

                DECISION = "Okay! I buy this!"
                tracking_dict = {"Key": [], "Aspect": []}
                conv_dict_13['conv_' + str(index + 1)]['pair_6'] = DECISION
            except:
                conv_dict_13['conv_' + str(index + 1)] = {}
                tracking_dict = {"Key": [], "Aspect": []}
                continue
    counter = 0
    conv_dict = {}
    for key in list(conv_dict_13.keys()):
        if conv_dict_13[str(key)]:
            counter += 1
            conv_dict['conv_' + str(counter)] = conv_dict_13[str(key)]
    return(conv_dict)


selected_item = 'B00FI8C9XK'
num_pairs = 20
conv_type_13_test = conv_type_13(selected_item, num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict)
conv_type_13_test['conv_1']


# ### Conversation Type #14

def conv_type_14(selected_item, num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict):
    conv_dict_14 = {}
    tracking_dict = {"Key": [], "Aspect": []}

    all_pairs_list_NP_IT = list(blocks_neg_100[selected_item]['Oneg1A_Opos1B_also_view'].keys())
    all_pairs_list_PP_QA_1 = list(blocks_neg_100[selected_item]['Qpos1A_Apos1A'].keys())

    if all_pairs_list_NP_IT and all_pairs_list_PP_QA_1:
        all_pairs_list_PP_AT = list(range(1, num_pairs))
        all_pairs_list_PP_QA_2 = list(range(1, num_pairs))

        all_pairs_combination = list(itertools.product(all_pairs_list_NP_IT, all_pairs_list_PP_QA_1, all_pairs_list_PP_AT, all_pairs_list_PP_QA_2))
        selected_pairs_combination = select_pairs_combination(all_pairs_combination, num_pairs)

        for index, selected_pair in enumerate(selected_pairs_combination):
            try:
                conv_dict_14['conv_' + str(index + 1)] = {}
                NP_IT = blocks_neg_100[selected_item]['Oneg1A_Opos1B_also_view'][selected_pair[0]]
                tracking_dict["Key"].append(NP_IT['Oneg1A']['Labels']['Key'])
                tracking_dict["Key"].append(NP_IT['Opos1B']['Labels']['Key'])
                aspect = NP_IT['Opos1B']['Labels']['Aspect']
                selected_item_B = NP_IT['Opos1B']['Labels']['Key'].split("_")[0]
                conv_dict_14['conv_' + str(index + 1)]['pair_1'] = NP_IT

                selected_pair_random = random.choice(list(blocks_neg_100[selected_item_B]['Qpos1A_Apos1A'].keys()))
                PP_QA = blocks_neg_100[selected_item_B]['Qpos1A_Apos1A'][selected_pair_random]
                if PP_QA['Qpos1A']['Labels']['Key'] not in tracking_dict["Key"]                 and PP_QA['Qpos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
                    tracking_dict["Key"].append(PP_QA['Qpos1A']['Labels']['Key'])
                    conv_dict_14['conv_' + str(index + 1)]['pair_2'] = PP_QA
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_14['conv_' + str(index + 1)] = {}
                    continue

                all_also_view_items = metaData_for_cellPhones[metaData_for_cellPhones.asin == selected_item_B].also_view.values[0]
                all_retrieved_index, all_retrieved_items = find_retrieved_items_and_index(retrieved_items_dict, selected_item_B)
                all_items_list = list(all_also_view_items) + all_retrieved_items
                all_items_list = list(set(all_items_with_review).intersection(all_items_list))

                selected_item_C = random.choice(all_items_list)

                selected_pair_random = random.choice(list(blocks_pos_100[selected_item_C]['Opos1B_Opos2B'].keys()))
                PP_AT = blocks_pos_100[selected_item_C]['Opos1B_Opos2B'][selected_pair_random]
                if PP_AT['Opos1B']['Labels']['Key'] not in tracking_dict["Key"] and PP_AT['Opos2B']['Labels']['Key'] not in tracking_dict["Key"]:
                    tracking_dict["Key"].append(PP_AT['Opos1B']['Labels']['Key'])
                    tracking_dict["Key"].append(PP_AT['Opos2B']['Labels']['Key'])
                    tracking_dict["Aspect"].append(PP_AT['Opos1B']['Labels']['Aspect'])
                    tracking_dict["Aspect"].append(PP_AT['Opos2B']['Labels']['Key'])
                    conv_dict_14['conv_' + str(index + 1)]['pair_3'] = PP_AT
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_14['conv_' + str(index + 1)] = {}
                    continue

                selected_pair_random = random.choice(list(blocks_neg_100[selected_item_C]['Qpos1A_Apos1A'].keys()))
                PP_QA = blocks_neg_100[selected_item_C]['Qpos1A_Apos1A'][selected_pair_random]
                if PP_QA['Qpos1A']['Labels']['Key'] not in tracking_dict["Key"]                 and PP_QA['Qpos1A']['Labels']['Aspect'] not in tracking_dict["Aspect"]:
                    conv_dict_14['conv_' + str(index + 1)]['pair_4'] = PP_QA
                else:
                    tracking_dict = {"Key": [], "Aspect": []}
                    conv_dict_14['conv_' + str(index + 1)] = {}
                    continue

                DECISION = "Okay! Great! I buy this!"
                tracking_dict = {"Key": [], "Aspect": []}
                conv_dict_14['conv_' + str(index + 1)]['pair_5'] = DECISION
            except:
                conv_dict_14['conv_' + str(index + 1)] = {}
                tracking_dict = {"Key": [], "Aspect": []}
                continue
    counter = 0
    conv_dict = {}
    for key in list(conv_dict_14.keys()):
        if conv_dict_14[str(key)]:
            counter += 1
            conv_dict['conv_' + str(counter)] = conv_dict_14[str(key)]
    return(conv_dict)

selected_item = 'B00FI8C9XK'
num_pairs = 20
conv_type_14_test = conv_type_14(selected_item, num_pairs, metaData_for_cellPhones, all_items_with_review, retrieved_items_dict)
conv_type_14_test['conv_9']