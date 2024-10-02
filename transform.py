import hashlib
import json

# Load data from a JSON file
with open('backup_26_sept_final_reviews_after_absa.json', 'r') as json_file:
    data = json.load(json_file)

# Function to generate a unique key
def generate_key(text, sentence):
    unique_string = text + sentence
    return hashlib.sha256(unique_string.encode()).hexdigest()[:22]  # Shorten hash for readability

# Function to transform data with multiple aspects and sentiments
def transform_data(data, limit=None):
    transformed_data = []
    counter = 0
    
    for entry in data:
        aspects = entry.get("aspect", [])
        sentiments = entry.get("sentiment", [])
        
        # If there are multiple aspects or sentiments, create new entries for each
        max_len = max(len(aspects), len(sentiments))
        if max_len > 1:
            for i in range(max_len):
                new_entry = entry.copy()
                new_entry["aspect"] = [aspects[i]] if i < len(aspects) else []
                new_entry["sentiment"] = [sentiments[i]] if i < len(sentiments) else []
                transformed_data.append(new_entry)
        else:
            transformed_data.append(entry)
        
        counter += 1
        
        # Stop if a limit is set and reached
        if limit and counter >= limit:
            break
    
    return transformed_data

# Transform the loaded data
transformed_entries = transform_data(data)

# Group transformed entries by 'asin' and generate unique keys
transformed_data = {}
for entry in transformed_entries:
    asin = entry['asin']
    key = generate_key(entry['text'], entry['sentence'])
    
    if asin not in transformed_data:
        transformed_data[asin] = []
    
    transformed_data[asin].append({
        key: {
            "sentence": entry["sentence"],
            "text": entry["text"],
            "aspect": entry["aspect"],
            "sentiment": entry["sentiment"],
            "asin": entry["asin"],
            "user_id": entry["user_id"]
        }
    })

# Save the transformed data to a JSON file
with open('transformed_data.json', 'w') as json_file:
    json.dump(transformed_data, json_file, indent=4)

print("Data transformation complete and saved to transformed_data.json")
