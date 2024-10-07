import json

file_path = "/home/stud/abedinz1/localDisk/opinionconv-refactor/100_blocks_neg.json"

# Read and load each line as a separate JSON object
with open(file_path, 'r') as f:
    data = []
    for line in f:
        try:
            # Load each line as a JSON object
            json_object = json.loads(line)
            data.append(json_object)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON on line: {e}")

# Now, `data` contains a list of all JSON objects
print(type(data))  # This should be a list
print(f"Number of items loaded: {len(data)}")

# Check the keys of the first JSON object (if any data was loaded)
if data:
    print(data[0].keys())
