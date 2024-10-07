import pandas as pd
import pprint as pp
import json

data = pd.read_pickle(r'Cellphone_sentiment_aspect_dict_100.pkl')

#orignal_data = pd.read_json('final_reviews_after_absa.json')

with open('final_reviews_after_absa.json', 'r') as f:
    orignal_data = json.loads(f)

pp.pp(type(orignal_data))
pp.pp(orignal_data)

orignal_data_with_single_aspect = []

for entry in orignal_data:
    aspects = entry.get("aspect", [])
    sentiments = entry.get("sentiment", [])
    
    # If there are multiple aspects or sentiments, create new entries for each
    max_len = max(len(aspects), len(sentiments))
    if max_len > 1:
        for i in range(max_len):
            new_entry = entry.copy()
            new_entry["aspect"] = [aspects[i]] if i < len(aspects) else []
            new_entry["sentiment"] = [sentiments[i]] if i < len(sentiments) else []
            orignal_data_with_single_aspect.append(new_entry)
    else:
        orignal_data_with_single_aspect.append(entry)

pp.pp(orignal_data_with_single_aspect)

