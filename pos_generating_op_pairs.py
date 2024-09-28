
def Opos1B_Opos2B(item, wrong_aspects, correct_forms, Opos1B_list, Opos2B_list, dict_AspectSentiment):
    blocks = {}
    counter = 0
    aspect_review_polarity_key_list = []
    item_review_list = dict_AspectSentiment.get(item)
    
    if item_review_list:
        # Collect all positive reviews for aspects in `aspect_review_polarity_key_list`
        for review_dict in item_review_list:
            for item_reviewer_aspect_key, review_sentiment in review_dict.items():
                key = review_sentiment["asin"] + '_' + review_sentiment["user_id"] + '_' + item_reviewer_aspect_key
                aspects = review_sentiment.get('aspect', [])  # Handle empty aspect list
                sentiments = review_sentiment.get('sentiment', [])  # Handle empty sentiment list
                review = cleaning_review(review_sentiment['sentence'])
                
                if aspects:
                    for aspect, polarity in zip(aspects, sentiments):
                        aspect = cleaning_aspect(aspect)
                        if aspect not in wrong_aspects and aspect is not None and str(polarity).lower() == 'positive':
                            aspect_review_polarity_key_list.append((aspect, review, polarity, key))
    
    # Process the aspects again and generate positive opinion blocks
    if item_review_list:
        for review_dict in item_review_list:
            for item_reviewer_aspect_key, review_sentiment in review_dict.items():
                key = review_sentiment["asin"] + '_' + review_sentiment["user_id"] + '_' + item_reviewer_aspect_key
                aspects = review_sentiment.get('aspect', [])  # Handle empty aspect list
                sentiments = review_sentiment.get('sentiment', [])  # Handle empty sentiment list
                review = cleaning_review(review_sentiment['sentence'])
                
                if aspects:
                    for aspect, polarity in zip(aspects, sentiments):
                        aspect = cleaning_aspect(aspect)
                        if aspect is not None and aspect not in wrong_aspects and str(polarity).lower() == 'positive':
                            Opos1B = random.choice(Opos1B_list).format(aspect) + review
                            
                            # Now generate the Opos2B opinion
                            for aspect_, review_, polarity_, key_ in aspect_review_polarity_key_list:
                                aspect_ = cleaning_aspect(aspect_)
                                if str(polarity_).lower() == 'positive' and str(review) != str(review_):
                                    counter += 1
                                    Opos2B = random.choice(Opos2B_list).format(aspect, aspect_) + review_

                                    blocks[f"Opos1B_Opos2B_{counter}"] = {
                                        'Opos1B': {
                                            'Opinion': Opos1B,
                                            'Labels': {
                                                'Key': key,
                                                'Aspect': aspect,
                                                'Polarity': str(polarity).lower()
                                            }
                                        },
                                        'Opos2B': {
                                            'Opinion': Opos2B,
                                            'Labels': {
                                                'Key': key_,
                                                'Aspect': aspect_,
                                                'Polarity': str(polarity_).lower()
                                            }
                                        }
                                    }
    return blocks


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
                key = review_sentiment["asin"] + '_' + review_sentiment["user_id"] + '_' + item_reviewer_aspect_key
                aspects = review_sentiment.get('aspect', [])  # Handle empty aspect list
                sentiments = review_sentiment.get('sentiment', [])  # Handle empty sentiment list
                review = cleaning_review(review_sentiment['sentence'])

                if aspects:
                    for (aspect, polarity) in zip(aspects, sentiments):
                        aspect = cleaning_aspect(aspect)
                        if aspect not in wrong_aspects and aspect != None and str(polarity).lower() == 'positive':
                                aspect_review_polarity_key_list.append((aspect, review, polarity, key))
                        
    if item_review_list:
        for review_dict in item_review_list:
            for item_reviewer_aspect_key, review_sentiment in (review_dict.items()):
                key = review_sentiment["asin"] + '_' + review_sentiment["user_id"] + '_' + item_reviewer_aspect_key
                aspects = review_sentiment.get('aspect', [])  # Handle empty aspect list
                sentiments = review_sentiment.get('sentiment', [])  # Handle empty sentiment list
                review = cleaning_review(review_sentiment['sentence'])

                if aspects:
                    for (aspect, polarity) in zip(aspects,sentiments):
                        aspect = cleaning_aspect(aspect)
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
                key = review_sentiment["asin"] + '_' + review_sentiment["user_id"] + '_' + item_reviewer_aspect_key
                aspects = review_sentiment.get('aspect', [])  # Handle empty aspect list
                sentiments = review_sentiment.get('sentiment', [])  # Handle empty sentiment list
                review = cleaning_review(review_sentiment['sentence'])

                if aspects:
                    for (aspect, polarity) in zip(aspects, sentiments):
                        aspect = cleaning_aspect(aspect)
                        if aspect not in wrong_aspects and aspect != None:
                            if str(polarity).lower() == 'negative':
                                aspect_review_polarity_key_list.append((aspect, review, polarity, key))
                        
    if item_review_list:
        for review_dict in item_review_list:
            for item_reviewer_aspect_key, review_sentiment in (review_dict.items()):
                kkey = review_sentiment["asin"] + '_' + review_sentiment["user_id"] + '_' + item_reviewer_aspect_key
                aspects = review_sentiment.get('aspect', [])  # Handle empty aspect list
                sentiments = review_sentiment.get('sentiment', [])  # Handle empty sentiment list
                review = cleaning_review(review_sentiment['sentence'])

                if aspects:
                    for (aspect, polarity) in zip(aspects, sentiments):
                        aspect = cleaning_aspect(aspect)
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


import json
import pickle

save_interval = 10  # Save after every 10 items
counter = 0  # Counter to track how many items have been processed since the last save

save_path_json = './100_blocks_pos.json'
save_path_pkl = './done_items_pos.pkl'

# Load previous progress if available
try:
    with open(save_path_pkl, 'rb') as fp:
        done_items_neg = pickle.load(fp)
except (FileNotFoundError, EOFError):
    done_items_neg = []

# Start the JSON file if it's the first time writing
try:
    with open(save_path_json, 'r') as f:
        # Check if the file has content; continue if it exists
        pass
except (FileNotFoundError, json.JSONDecodeError):
    # If the file doesn't exist, initialize it with an opening curly brace
    with open(save_path_json, 'w') as f:
        f.write("{\n")

# Function to append a batch of key-value pairs to the JSON file
def append_to_json_file(file_path, batch_dict):
    with open(file_path, 'a') as f:
        for key, value in batch_dict.items():
            # Dump key-value pair and add a comma and newline
            json.dump({key: value}, f)
            f.write(",\n")

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

                # Append item data to the JSON file and free memory
                append_to_json_file(save_path_json, {str(item): item_data})
                counter += 1

                # Save progress every 10 items in the pickle file for done_items_neg
                if counter % save_interval == 0:
                    with open(save_path_pkl, 'wb') as fp:
                        pickle.dump(done_items_neg, fp, protocol=4)
                    print(f"Progress saved after processing {counter} items.")

                # Free memory after processing each item
                del item_data

# Finalize the JSON by removing the last comma and closing the structure
with open(save_path_json, 'rb+') as f:
    f.seek(0, 2)  # Move the pointer to the end of the file
    f.seek(f.tell() - 2, 0)  # Move back two positions to remove the last comma
    f.truncate()  # Remove the last comma
    f.write(b"\n}")  # Close the JSON dictionary

# Final save for done_items_neg
with open(save_path_pkl, 'wb') as fp:
    pickle.dump(done_items_neg, fp, protocol=4)

print("Final progress saved!")
