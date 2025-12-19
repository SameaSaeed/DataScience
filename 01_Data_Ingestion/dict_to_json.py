import json
from datetime import datetime

def create_library_data():
    """
    Create a dictionary representing library data
    """
    library_data = {
        "library_name": "Central University Library",
        "location": "Main Campus",
        "established": 1965,
        "total_books": 150000,
        "digital_resources": True,
        "operating_hours": {
            "monday_friday": "8:00 AM - 10:00 PM",
            "saturday": "9:00 AM - 6:00 PM",
            "sunday": "12:00 PM - 8:00 PM"
        },
        "departments": [
            {
                "name": "Reference",
                "floor": 1,
                "staff_count": 5,
                "services": ["Research Help", "Citation Assistance", "Database Access"]
            },
            {
                "name": "Circulation",
                "floor": 1,
                "staff_count": 8,
                "services": ["Book Checkout", "Returns", "Renewals", "Holds"]
            },
            {
                "name": "Digital Media",
                "floor": 2,
                "staff_count": 3,
                "services": ["Computer Access", "Printing", "Scanning", "Media Equipment"]
            }
        ],
        "popular_books": [
            {
                "title": "Introduction to Algorithms",
                "author": "Thomas H. Cormen",
                "isbn": "978-0262033848",
                "checkout_count": 245,
                "available_copies": 3
            },
            {
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "isbn": "978-0132350884",
                "checkout_count": 189,
                "available_copies": 5
            }
        ],
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return library_data

def dict_to_json_string(data, indent=None):
    """
    Convert dictionary to JSON string
    """
    try:
        json_string = json.dumps(data, indent=indent)
        return json_string
    except TypeError as e:
        print(f"Error converting to JSON: {e}")
        return None

def write_json_to_file(data, filename):
    """
    Write dictionary data to JSON file
    """
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Successfully wrote data to {filename}")
        return True
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False

def main():
    # Create dictionary data
    library_data = create_library_data()
    
    print("ORIGINAL DICTIONARY DATA:")
    print("=" * 40)
    print(f"Type: {type(library_data)}")
    print(f"Library Name: {library_data['library_name']}")
    print(f"Total Books: {library_data['total_books']}")
    print(f"Number of Departments: {len(library_data['departments'])}")
    
    # Convert to JSON string (compact format)
    print("\nJSON STRING (COMPACT):")
    print("=" * 40)
    json_compact = dict_to_json_string(library_data)
    if json_compact:
        print(json_compact[:200] + "..." if len(json_compact) > 200 else json_compact)
    
    # Convert to JSON string (formatted)
    print("\nJSON STRING (FORMATTED):")
    print("=" * 40)
    json_formatted = dict_to_json_string(library_data, indent=2)
    if json_formatted:
        print(json_formatted[:500] + "..." if len(json_formatted) > 500 else json_formatted)
    
    # Write to file
    print("\nWRITING TO FILE:")
    print("=" * 40)
    success = write_json_to_file(library_data, "library_data.json")
    
    if success:
        # Verify by reading back
        print("\nVERIFYING FILE CONTENTS:")
        print("=" * 40)
        try:
            with open("library_data.json", 'r') as file:
                loaded_data = json.load(file)
                print(f"Successfully loaded {len(loaded_data)} keys from file")
                print(f"Library name from file: {loaded_data['library_name']}")
        except Exception as e:
            print(f"Error reading file: {e}")

if __name__ == "__main__":
    main()