def process_student_data(filename):
    """
    Process student data and calculate statistics
    """
    students = []
    subjects = {}
    grades = []
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                clean_line = line.strip()
                if clean_line:
                    parts = clean_line.split(' - ')
                    if len(parts) == 3:
                        name = parts[0]
                        subject = parts[1]
                        grade_str = parts[2].replace('Grade: ', '')
                        
                        # Store student information
                        student_info = {
                            'name': name,
                            'subject': subject,
                            'grade': grade_str
                        }
                        students.append(student_info)
                        
                        # Count subjects
                        if subject in subjects:
                            subjects[subject] += 1
                        else:
                            subjects[subject] = 1
                        
                        # Convert grades to numerical values for statistics
                        grade_value = convert_grade_to_number(grade_str)
                        if grade_value is not None:
                            grades.append(grade_value)
        
        # Display results
        print(f"Total students: {len(students)}")
        print("\nSubject distribution:")
        for subject, count in subjects.items():
            print(f"  {subject}: {count} students")
        
        if grades:
            avg_grade = sum(grades) / len(grades)
            print(f"\nAverage grade (numerical): {avg_grade:.2f}")
            print(f"Highest grade: {max(grades)}")
            print(f"Lowest grade: {min(grades)}")
        
        return students, subjects, grades
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return [], {}, []
    except Exception as e:
        print(f"Error processing file: {e}")
        return [], {}, []

def convert_grade_to_number(grade_str):
    """
    Convert letter grades to numerical values
    """
    grade_map = {
        'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1.0,
        'F': 0.0
    }
    return grade_map.get(grade_str, None)

def main():
    filename = "students.txt"
    students, subjects, grades = process_student_data(filename)

if __name__ == "__main__":
    main()