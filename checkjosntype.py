import json

# Load the downloaded JSON file with specified encoding
with open('all_companies.json', 'r', encoding='utf-8', errors='ignore') as f:
    data = json.load(f)

# Check the structure of the loaded JSON data
print(type(data))  # Print the type of data
print(data[:2])    # Print the first two items if it's a list
