import pandas as pd
import json
import pickle
import re
import random

metaData_for_cellPhones = pd.read_pickle("./metaData_for_cellPhones.pkl") #source: MAIN.py
wrong_aspects_3 = pd.read_pickle('./wrong_aspects_3.pkl')

# Path to the input JSON file
input_file = 'transformed_data.json'

# Read the JSON file
with open(input_file, 'r') as f:
    dict_AspectSentiment = json.load(f)


with open("./retrieved_items_dict.json") as f:     #source: MAIN.py
    retrieved_items_dict = json.load(f)
retrieved_items_dict


wrong_aspects = wrong_aspects_3 + ["lumia 1020", "zero key", "verizon", 'back', 'edge', 'feel', 'phone', 'seller']

correct_forms = ['bluetooth']

Q1A_list = ["What do you think about its {}?", "May I know your opinion on its {}?",
            "What about its {}?", "Do you have any views on its {}?",
            "Could you tell me your opinion on its {}?",
            "Do you have any opinions about its {}?", "In your honest opinion, how is its {}?",
            "Can you give me your thoughts on its {}?", "I’d like to know your views on its {}.",
            "Do you have any particular views on its {}?", "From your point of view, how is the {}?",
            "I’d be very interested to know your views on its {}."
           ]

Oneg1A_list = ["I heard about its {} that ",
               "I was told by one of my friends about its {} that ",
               "As far as I know about its {}, ",
               "What I know about its {} is that "]

Opos1A_list = ["No, I don't think so, because ",
               "Let me disagree with you, because ",
               "I see your point, but ",
               "I see what you mean, but "]

# For MultiWOZ
#Opos1B_list = ["If {} is important for you, we can offer this item. ", 
#               "If {} is a crucial feature for you, we have this item. "]

Opos1B_list = ["If {} is important for you, we can offer this item: {} ", 
               "If {} is a crucial feature for you, we have this item: {} "]

Opos2A_list = ["I can see what you’re saying but I disagree with you on its {} and even I can tell you something interesting about this phone and its {} that ",
               "I’m sorry but I don’t think so, specially about its {} and I would mention something about the {} of this phone that "]

# For MultiWOZ
#Opos1B1_list = ["I heard about this phone and specially its {} that ",
#               "I was told by one of my friends about this phone and its {} that ",
#               "I was wondering if you have this phone, it might be a good choice because as far as I know about its {}, "]

Opos1B1_list = ["I heard about this phone {} and specially its {} that ",
                "I was told by one of my friends about this phone {} and its {} that ",
                "I was wondering if you have this phone {}, it might be a good choice because as far as I know about its {}, "]

Opos1B2_list = ["Yes, it's true! This phone is also a good choice.",
                "Yes, That's so true. This phone is also a good choice.",
                "Yes, That's for sure. This phone is also a good choice.",
                "Yes, I think so too. This phone is also a good choice.",
                "Yes, That is what I think too. This phone is also a good choice.",
                "Yes! I agree with you. This phone is also a good choice.",
                "Yes, I agree with you about it. This phone is also a good choice.",
                "Yes, That's exactly what I know about it. This phone is also a good choice."]

Opos2B_list = ["Yes, it's true! This phone is also a good choice and even I can tell you something interesting about this phone and its {} that ",
               "Yes, That's so true. This phone is also a good choice and I would mention something about the {} of this phone that ",
               "Yes, That's for sure. This phone is also a good choice and even I can tell you something interesting about this phone and its {} that ",
               "Yes, I think so too. This phone is also a good choice and I would mention something about the {} of this phone that ",
               "Yes, That is what I think too. This phone is also a good choice and even I can tell you something interesting about this phone and its {} that ",
               "Yes! I agree with you. This phone is also a good choice and I would mention something about the {} of this phone that ",
               "Yes, I agree with you about it. This phone is also a good choice and even I can tell you something interesting about this phone and its {} that ",
               "Yes, That's exactly what I know about it. This phone is also a good choice and I would mention something about the {} of this phone that "]

Oneg2B_list = ["Yes, it's true! This phone might be a good choice but you should know about its {} that ",
               "Yes, That's so true. This phone can be also a good choice but I should say about the {} of this phone that ",
               "Yes, That's for sure. This phone is also a good choice However about the {} of this phone I should say that ",
               "Yes, I completely agree with you. This phone might be a good choice but you should know about its {} that ",
               "Yes, I totally agree with you. This phone can be also a good choice but I should say about the {} of this phone that ",
               "Yes! I agree with you. This phone is also a good choice However about the {} of this phone I should say that ",
               "Yes, I agree with you about it. This phone can be also a good choice but I should say about the {} of this phone that ",
               "Yes, That's exactly what I know about it. However I should say something about the {} of this phone that "]


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



def Qpos1A_Apos1A(item, wrong_aspects, correct_forms, Q11_list, dict_AspectSentiment):
    blocks = {}
    counter = 0
    item_review_list = dict_AspectSentiment.get(item)
    #print("yaar item_review_list: ",item_review_list)
    if item_review_list:
        #print("hiba is here")
        for review_dict in item_review_list:
            #print("zain is here")
            for unique_id, review_sentiment in (review_dict.items()):
                #print("unique_id: ",unique_id)
                #print("review_sentiment: ",review_sentiment)
                aspect = review_sentiment['aspect']
                #aspect = cleaning_aspect(aspect)
                review = review_sentiment['text']
                #review = cleaning_review(review)
                polarity = review_sentiment['sentiment'][0] if len(review_sentiment['sentiment']) else 'negative'
                print("polarity: ",polarity)
                if aspect not in wrong_aspects and aspect != None:
                    if str(polarity).lower() == 'positive':
                        counter += 1
                        #aspect = cleaning_aspect(str(aspect))
                        
                        Qpos1A = random.choice(Q1A_list).format(aspect)
                        Apos1A = review
                        print("polarity inside:",polarity)
                        blocks["Qpos1A_Apos1A_" + str(counter)] = {}
                        blocks["Qpos1A_Apos1A_" + str(counter)]['Qpos1A'] = {}
                        blocks["Qpos1A_Apos1A_" + str(counter)]['Qpos1A']['Question'] = Qpos1A
                        blocks["Qpos1A_Apos1A_" + str(counter)]['Qpos1A']['Labels'] = {}
                        blocks["Qpos1A_Apos1A_" + str(counter)]['Qpos1A']['Labels']['Key'] = unique_id
                        blocks["Qpos1A_Apos1A_" + str(counter)]['Qpos1A']['Labels']['Aspect'] = aspect
                        blocks["Qpos1A_Apos1A_" + str(counter)]['Qpos1A']['Labels']['Polarity'] = str(polarity).lower()
                        
                        blocks["Qpos1A_Apos1A_" + str(counter)]['Apos1A'] = {}
                        blocks["Qpos1A_Apos1A_" + str(counter)]['Apos1A']['Answer'] = Apos1A
                        blocks["Qpos1A_Apos1A_" + str(counter)]['Apos1A']['Labels'] = {}
                        blocks["Qpos1A_Apos1A_" + str(counter)]['Apos1A']['Labels']['Key'] = unique_id
                        blocks["Qpos1A_Apos1A_" + str(counter)]['Apos1A']['Labels']['Aspect'] = aspect
                        blocks["Qpos1A_Apos1A_" + str(counter)]['Apos1A']['Labels']['Polarity'] = str(polarity).lower()
                        print("yooo")
                        #print("BLOCK")
                        #print(blocks)
    return(blocks)

def Oneg1A_Opos1A(item, wrong_aspects, correct_forms, Oneg1A_list, Opos1A_list, dict_AspectSentiment):
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
                review = review_sentiment['text']
                review = cleaning_review(review)
                polarity = review_sentiment['sentiment']
                if aspect not in wrong_aspects and aspect != None:
                    if str(polarity).lower() == 'positive':
                        aspect_review_polarity_key_list.append((aspect, review, polarity, key))

        for review_dict in item_review_list:
            print(review_dict)
            for item_reviewer_aspect_key, review_sentiment in (review_dict.items()):
                key = item_reviewer_aspect_key[0]
                aspect = item_reviewer_aspect_key[1]
                review = review_sentiment['text']
                review = cleaning_review(review)
                polarity = review_sentiment['sentiment']
                if aspect != None and aspect not in wrong_aspects:
                    if str(polarity).lower() == 'negative':
                        sentence_aspect = review
                        
                        Oneg1A = random.choice(Oneg1A_list).format(aspect) + sentence_aspect
                        
                        for aspect_, review_, polarity_, key_ in aspect_review_polarity_key_list:
                            aspect_ = cleaning_aspect(aspect_)
                                
                            if str(polarity_).lower() == 'positive' and np.logical_or(str(aspect) == str(aspect_), aspects_similarity_check(aspect, aspect_, similar_aspect_list)):
                                counter += 1
                                sentence_aspect_ = review_

                                Opos1A = random.choice(Opos1A_list) + sentence_aspect_

                                blocks["Oneg1A_Opos1A_" + str(counter)] = {}
                                blocks["Oneg1A_Opos1A_" + str(counter)]['Oneg1A'] = {}
                                blocks["Oneg1A_Opos1A_" + str(counter)]['Oneg1A']['Opinion'] = Oneg1A
                                blocks["Oneg1A_Opos1A_" + str(counter)]['Oneg1A']['Labels'] = {}
                                blocks["Oneg1A_Opos1A_" + str(counter)]['Oneg1A']['Labels']['Key'] = key
                                blocks["Oneg1A_Opos1A_" + str(counter)]['Oneg1A']['Labels']['Aspect'] = aspect
                                blocks["Oneg1A_Opos1A_" + str(counter)]['Oneg1A']['Labels']['Polarity'] = str(polarity).lower()

                                blocks["Oneg1A_Opos1A_" + str(counter)]['Opos1A'] = {}
                                blocks["Oneg1A_Opos1A_" + str(counter)]['Opos1A']['Opinion'] = Opos1A
                                blocks["Oneg1A_Opos1A_" + str(counter)]['Opos1A']['Labels'] = {}
                                blocks["Oneg1A_Opos1A_" + str(counter)]['Opos1A']['Labels']['Key'] = key_
                                blocks["Oneg1A_Opos1A_" + str(counter)]['Opos1A']['Labels']['Aspect'] = aspect_
                                blocks["Oneg1A_Opos1A_" + str(counter)]['Opos1A']['Labels']['Polarity'] = str(polarity_).lower()
    return(blocks)

def Oneg1A_Opos1B(item, retrieved_items, wrong_aspects, correct_forms, Oneg1A_list, Opos1B_list, dict_AspectSentiment, DF, retrieved=True, also_view=False):
    blocks = {}
    counter = 0
    similarity = 0
    item_1 = item
    if retrieved:
        other_items_list = [i for i in retrieved_items if i != item_1]
    elif also_view:
        if DF.query("asin == @item_1").bought_together.values.size > 0:
            other_items_list = DF.query("asin == @item_1").bought_together.values[0]
        else:
            other_items_list = None
    if other_items_list:
        aspect_review_polarity_key_lists = []
        for item_2 in other_items_list:
            item_2_review_list = dict_AspectSentiment.get(item_2)
            if item_2_review_list:
                aspect_review_polarity_key_list = []
                for item_2_review_dict in item_2_review_list:
                    for item_2_reviewer_aspect_key, item_2_review_sentiment in (item_2_review_dict.items()):
                        item_2_key = item_2_reviewer_aspect_key[0]
                        item_2_aspect = item_2_reviewer_aspect_key[1]
                        item_2_aspect = cleaning_aspect(item_2_aspect)
                        item_2_review = item_2_review_sentiment['text']
                        item_2_review = cleaning_review(item_2_review)
                        item_2_polarity = item_2_review_sentiment['sentiment']
                        if item_2_aspect not in wrong_aspects and item_2_aspect != None:
                            if str(item_2_polarity).lower() == 'positive':
                                aspect_review_polarity_key_list.append((item_2, item_2_aspect, item_2_review, item_2_polarity, item_2_key))

                aspect_review_polarity_key_lists.append(aspect_review_polarity_key_list)


        item_1_review_list = dict_AspectSentiment.get(item_1)
        if item_1_review_list:
            for item_1_review_dict in item_1_review_list:
                for item_1_reviewer_aspect_key, item_1_review_sentiment in (item_1_review_dict.items()):
                    item_1_key = item_1_reviewer_aspect_key[0]
                    item_1_aspect = item_1_reviewer_aspect_key[1]
                    item_1_aspect = cleaning_aspect(item_1_aspect)
                    item_1_review = item_1_review_sentiment['text']
                    item_1_review = cleaning_review(item_1_review)
                    item_1_polarity = item_1_review_sentiment['sentiment']
                    if item_1_aspect != None and item_1_aspect not in wrong_aspects:
                        if str(item_1_polarity).lower() == 'negative':
                            Oneg1A = random.choice(Oneg1A_list).format(item_1_aspect) + item_1_review

                            for item_aspect_review_polarity_key in aspect_review_polarity_key_lists:
                                for item_, aspect_, review_, polarity_, key_ in item_aspect_review_polarity_key:
                                    aspect_ = cleaning_aspect(aspect_)

                                    if str(polarity_).lower() == 'positive' and np.logical_or(str(item_1_aspect) == str(aspect_), aspects_similarity_check(item_1_aspect, aspect_, similar_aspect_list)):
                                        counter += 1
                                        
                                        
                                        Opos1B = random.choice(Opos1B_list).format(item_1_aspect, item_) + review_
                                        #For MultiWOZ
                                        #Opos1B = random.choice(Opos1B_list).format(item_1_aspect) + review_

                                        blocks["Oneg1A_Opos1B_" + str(counter)] = {}
                                        blocks["Oneg1A_Opos1B_" + str(counter)]['Oneg1A'] = {}
                                        blocks["Oneg1A_Opos1B_" + str(counter)]['Oneg1A']['Opinion'] = Oneg1A
                                        blocks["Oneg1A_Opos1B_" + str(counter)]['Oneg1A']['Labels'] = {}
                                        blocks["Oneg1A_Opos1B_" + str(counter)]['Oneg1A']['Labels']['Key'] = item_1_key
                                        blocks["Oneg1A_Opos1B_" + str(counter)]['Oneg1A']['Labels']['Aspect'] = item_1_aspect
                                        blocks["Oneg1A_Opos1B_" + str(counter)]['Oneg1A']['Labels']['Polarity'] = str(item_1_polarity).lower()

                                        blocks["Oneg1A_Opos1B_" + str(counter)]['Opos1B'] = {}
                                        blocks["Oneg1A_Opos1B_" + str(counter)]['Opos1B']['Opinion'] = Opos1B
                                        blocks["Oneg1A_Opos1B_" + str(counter)]['Opos1B']['Labels'] = {}
                                        blocks["Oneg1A_Opos1B_" + str(counter)]['Opos1B']['Labels']['Key'] = key_
                                        blocks["Oneg1A_Opos1B_" + str(counter)]['Opos1B']['Labels']['Aspect'] = aspect_
                                        blocks["Oneg1A_Opos1B_" + str(counter)]['Opos1B']['Labels']['Polarity'] = str(polarity_).lower()
                                    
    return(blocks)

def Oneg1A_Opos2A(item, wrong_aspects, correct_forms, Oneg1A_list, Opos2A_list, dict_AspectSentiment, restricted_version=True):
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
                review = review_sentiment['text']
                review = cleaning_review(review)
                polarity = review_sentiment['sentiment']
                if aspect not in wrong_aspects and aspect != None:
                    if str(polarity).lower() == 'positive':
                        aspect_review_polarity_key_list.append((aspect, review, polarity, key))

        for review_dict in item_review_list:
            for item_reviewer_aspect_key, review_sentiment in (review_dict.items()):
                key = item_reviewer_aspect_key[0]
                aspect = item_reviewer_aspect_key[1]
                aspect = cleaning_aspect(aspect)
                review = review_sentiment['text']
                review = cleaning_review(review)
                polarity = review_sentiment['sentiment']
                if aspect != None and aspect not in wrong_aspects:
                    if str(polarity).lower() == 'negative':
                        
                        Oneg1A = random.choice(Oneg1A_list).format(aspect) + review
                        
                        check = False 
                        # We disagree with the user only when there is a positive review for the aspect, mentioned by user
                        if restricted_version == True:
                            for aspect_, review_, polarity_, key_ in aspect_review_polarity_key_list:
                                if check == False:
                                    aspect_ = cleaning_aspect(aspect_)

                                    if str(polarity_).lower() == 'positive' and np.logical_or(str(aspect) == str(aspect_), aspects_similarity_check(aspect, aspect_, similar_aspect_list)):
                                        check = True
                                        break
                            
                            if check == True:
                                for aspect_, review_, polarity_, key_ in aspect_review_polarity_key_list:
                                    aspect_ = cleaning_aspect(aspect_)
                                    if str(polarity_).lower() == 'positive':
                                        counter += 1

                                        Opos2A = random.choice(Opos2A_list).format(aspect, aspect_) + review_

                                        blocks["Oneg1A_Opos2A_" + str(counter)] = {}
                                        blocks["Oneg1A_Opos2A_" + str(counter)]['Oneg1A'] = {}
                                        blocks["Oneg1A_Opos2A_" + str(counter)]['Oneg1A']['Opinion'] = Oneg1A
                                        blocks["Oneg1A_Opos2A_" + str(counter)]['Oneg1A']['Labels'] = {}
                                        blocks["Oneg1A_Opos2A_" + str(counter)]['Oneg1A']['Labels']['Key'] = key
                                        blocks["Oneg1A_Opos2A_" + str(counter)]['Oneg1A']['Labels']['Aspect'] = aspect
                                        blocks["Oneg1A_Opos2A_" + str(counter)]['Oneg1A']['Labels']['Polarity'] = str(polarity).lower()

                                        blocks["Oneg1A_Opos2A_" + str(counter)]['Opos2A'] = {}
                                        blocks["Oneg1A_Opos2A_" + str(counter)]['Opos2A']['Opinion'] = Opos2A
                                        blocks["Oneg1A_Opos2A_" + str(counter)]['Opos2A']['Labels'] = {}
                                        blocks["Oneg1A_Opos2A_" + str(counter)]['Opos2A']['Labels']['Key'] = key_
                                        blocks["Oneg1A_Opos2A_" + str(counter)]['Opos2A']['Labels']['Aspect'] = aspect_
                                        blocks["Oneg1A_Opos2A_" + str(counter)]['Opos2A']['Labels']['Polarity'] = str(polarity_).lower()
                        
                        else:
                            for aspect_, review_, polarity_, key_ in aspect_review_polarity_key_list:
                                aspect_ = cleaning_aspect(aspect_)
                                if str(polarity_).lower() == 'positive':
                                    counter += 1

                                    Opos2A = random.choice(Opos2A_list).format(aspect, aspect_) + review_

                                    blocks["Oneg1A_Opos2A_" + str(counter)] = {}
                                    blocks["Oneg1A_Opos2A_" + str(counter)]['Oneg1A'] = {}
                                    blocks["Oneg1A_Opos2A_" + str(counter)]['Oneg1A']['Opinion'] = Oneg1A
                                    blocks["Oneg1A_Opos2A_" + str(counter)]['Oneg1A']['Labels'] = {}
                                    blocks["Oneg1A_Opos2A_" + str(counter)]['Oneg1A']['Labels']['Key'] = key
                                    blocks["Oneg1A_Opos2A_" + str(counter)]['Oneg1A']['Labels']['Aspect'] = aspect
                                    blocks["Oneg1A_Opos2A_" + str(counter)]['Oneg1A']['Labels']['Polarity'] = str(polarity).lower()

                                    blocks["Oneg1A_Opos2A_" + str(counter)]['Opos2A'] = {}
                                    blocks["Oneg1A_Opos2A_" + str(counter)]['Opos2A']['Opinion'] = Opos2A
                                    blocks["Oneg1A_Opos2A_" + str(counter)]['Opos2A']['Labels'] = {}
                                    blocks["Oneg1A_Opos2A_" + str(counter)]['Opos2A']['Labels']['Key'] = key_
                                    blocks["Oneg1A_Opos2A_" + str(counter)]['Opos2A']['Labels']['Aspect'] = aspect_
                                    blocks["Oneg1A_Opos2A_" + str(counter)]['Opos2A']['Labels']['Polarity'] = str(polarity_).lower()
                                    
    return(blocks)



done_items_neg = []
all_blocks_neg = {}

for index in list(retrieved_items_dict.keys()):
    #print(str(index))
    retrieved_items_1 = retrieved_items_dict[str(index)].get("retrieved items")
    retrieved_items_with_review = [i for i in retrieved_items_1 if metaData_for_cellPhones.query("asin == @i").num_reviews.values[0] > 0]
    #print('retrieved_items_with_review:', retrieved_items_with_review)
    if len(retrieved_items_with_review) > 0:
        for item in retrieved_items_with_review:
            if item not in done_items_neg:
                done_items_neg.append(item)
                #print(item)
                all_blocks_neg[str(item)] = {}
                blocks_Qpos1A_Apos1A = Qpos1A_Apos1A(item, wrong_aspects, correct_forms, Q1A_list, dict_AspectSentiment)
                all_blocks_neg[str(item)]['Qpos1A_Apos1A'] = blocks_Qpos1A_Apos1A
                print("blocks_Qpos1A_Apos1A is DONE!")
                
                # blocks_Oneg1A_Opos1A = Oneg1A_Opos1A(item, wrong_aspects, correct_forms, Oneg1A_list, Opos1A_list, dict_AspectSentiment)
                # all_blocks_neg[str(item)]['Oneg1A_Opos1A'] = blocks_Oneg1A_Opos1A
                # print("blocks_Oneg1A_Opos1A is DONE!")

                # blocks_Oneg1A_Opos1B_retrieved = Oneg1A_Opos1B(item, retrieved_items_with_review, wrong_aspects, correct_forms, Oneg1A_list, Opos1B_list,
                #                                      dict_AspectSentiment, metaData_for_cellPhones, retrieved=True, also_view=False)
                # all_blocks_neg[str(item)]['Oneg1A_Opos1B_retrieved'] = blocks_Oneg1A_Opos1B_retrieved
                # print("blocks_Oneg1A_Opos1B_retrieved is DONE!")

                # blocks_Oneg1A_Opos1B_also_view = Oneg1A_Opos1B(item, retrieved_items_with_review, wrong_aspects, correct_forms, Oneg1A_list, Opos1B_list,
                #                                      dict_AspectSentiment, metaData_for_cellPhones, retrieved=False, also_view=True)
                # all_blocks_neg[str(item)]['Oneg1A_Opos1B_also_view'] = blocks_Oneg1A_Opos1B_also_view
                # print("blocks_Oneg1A_Opos1B_also_view is DONE!")

                # blocks_Oneg1A_Opos2A_restricted = Oneg1A_Opos2A(item, wrong_aspects, correct_forms, Oneg1A_list, Opos2A_list,
                #                                     dict_AspectSentiment, restricted_version=True)
                # all_blocks_neg[str(item)]['Oneg1A_Opos2A_restricted'] = blocks_Oneg1A_Opos2A_restricted
                # print("blocks_Oneg1A_Opos2A_restricted is DONE!")
                
                # blocks_Oneg1A_Opos2A_unrestricted = Oneg1A_Opos2A(item, wrong_aspects, correct_forms, Oneg1A_list, Opos2A_list,
                #                                                   dict_AspectSentiment, restricted_version=False)
                # all_blocks_neg[str(item)]['Oneg1A_Opos2A_unrestricted'] = blocks_Oneg1A_Opos2A_unrestricted
                # print("blocks_Oneg1A_Opos2A_unrestricted is DONE!")

with open('./100_blocks_neg.json', 'w') as f:
    json.dump(all_blocks_neg, f)

# with open('./done_items_neg.pkl', 'wb') as fp:
#     pickle.dump(done_items_neg, fp, protocol=4)