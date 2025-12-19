Best Practices for JSON Handling

1. Always Use Error Handling
try:
    with open('file.json', 'r') as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error: {e}")


2. Validate Data Structure
def validate_required_keys(data, required_keys):
    missing = [key for key in required_keys if key not in data]
    if missing:
        raise ValueError(f"Missing required keys: {missing}")


3. Use Pretty Printing for Debugging
import json
print(json.dumps(data, indent=2))


4. Handle Nested Structures Safely
# Safe navigation
value = data.get('level1', {}).get('level2', {}).get('level3', 'default')

5. TypeError: Object is not JSON serializable 
Convert datetime objects to strings
Handle custom objects with default parameter
Use str() for non-serializable types