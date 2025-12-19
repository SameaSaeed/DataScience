import json
import pprint

def read_json_file(filename):
    """
    Read a JSON file and return the parsed data
    """
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        return None

def display_student_info(student_data):
    """
    Display student information in a formatted way
    """
    if not student_data:
        return
    
    print("=" * 50)
    print("STUDENT INFORMATION")
    print("=" * 50)
    
    # Basic information
    print(f"Student ID: {student_data['student_id']}")
    print(f"Name: {student_data['name']}")
    print(f"Age: {student_data['age']}")
    print(f"Major: {student_data['major']}")
    print(f"GPA: {student_data['gpa']}")
    print(f"Status: {'Active' if student_data['active'] else 'Inactive'}")
    
    # Contact information
    print("\nCONTACT INFORMATION:")
    print("-" * 20)
    contact = student_data['contact']
    print(f"Email: {contact['email']}")
    print(f"Phone: {contact['phone']}")
    
    # Address
    address = contact['address']
    print(f"Address: {address['street']}")
    print(f"         {address['city']}, {address['state']} {address['zip']}")
    
    # Courses
    print("\nENROLLED COURSES:")
    print("-" * 20)
    for course in student_data['courses']:
        print(f"• {course['course_code']}: {course['course_name']}")
        print(f"  Credits: {course['credits']}, Grade: {course['grade']}")

def main():
    # Read the JSON file
    filename = "student_data.json"
    student_data = read_json_file(filename)
    
    if student_data:
        # Display formatted output
        display_student_info(student_data)
        
        # Also show raw JSON structure using pprint
        print("\n" + "=" * 50)
        print("RAW JSON STRUCTURE:")
        print("=" * 50)
        pprint.pprint(student_data, indent=2)

if __name__ == "__main__":
    main()