import pandas as pd
import pprint as pp
import json
from nanoid import generate


data = pd.read_pickle(r'Cellphone_sentiment_aspect_dict_100.pkl')


with open('final_reviews_after_absa.json', 'r') as f:
    orignal_data = json.load(f)

pp.pp(type(orignal_data))


orignal_data_with_single_aspect = []

for entry in orignal_data:
    aspects = entry.get("aspect", [])
    sentiments = entry.get("sentiment", [])
    
    # If there are multiple aspects or sentiments, create new entries for each
    max_len = max(len(aspects), len(sentiments))
    if max_len == 0:
        pass
    else:
        for i in range(max_len):
            key = generate()
            new_entry = entry.copy()
            new_entry["aspect"] = aspects[i]
            new_entry["sentiment"] = sentiments[i]
            new_entry["unique_key"] = key
            orignal_data_with_single_aspect.append(new_entry)

#pp.pp(orignal_data_with_single_aspect)

# Save the transformed_data_for_rag
with open('transformed_data_for_vector_database.json', 'w') as json_file:
    json.dump(orignal_data_with_single_aspect, json_file)


# Group transformed entries by 'asin' and generate unique keys
transformed_data = {}
for entry in orignal_data_with_single_aspect:
    asin = entry['asin']
    
    if asin not in transformed_data:
        transformed_data[asin] = []
    
    transformed_data[asin].append({
        entry["unique_key"]: {
            "sentence": entry["sentence"],
            "aspect": entry["aspect"],
            "sentiment": entry["sentiment"],
            "asin": entry["asin"],
            "user_id": entry["user_id"]
        }
    })

#pp.pp(transformed_data)
# Save the transformed data to a JSON file
with open('transformed_data_for_100_blocks.json', 'w') as json_file:
    json.dump(transformed_data, json_file)

print("Data transformation complete and saved to transformed_data.json")
