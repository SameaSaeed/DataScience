import os

def read_file_with_context_manager(filename):
    """
    File reading using context manager (with statement)
    """
    try:
        print(f"Attempting to read file: {filename}")
        with open(filename, 'r') as file:
            content = file.read()
            print(f"Successfully read {len(content)} characters")
            return content
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    
    except PermissionError:
        print(f"Error: No permission to read '{filename}'")
        return None
    
    except UnicodeDecodeError:
        print(f"Error: Unable to decode file '{filename}' - may contain binary data")
        return None
    
    except Exception as e:
        print(f"Unexpected error reading '{filename}': {type(e).__name__}: {e}")
        return None

def write_file_safely(filename, content):
    """
    Safe file writing with exception handling
    """
    try:
        print(f"Attempting to write to file: {filename}")
        with open(filename, 'w') as file:
            file.write(content)
            print(f"Successfully wrote {len(content)} characters to {filename}")
            return True
    
    except PermissionError:
        print(f"Error: No permission to write to '{filename}'")
        return False
    
    except OSError as e:
        print(f"Error: OS error occurred while writing to '{filename}': {e}")
        return False
    
    except Exception as e:
        print(f"Unexpected error writing to '{filename}': {type(e).__name__}: {e}")
        return False

def create_test_files():
    """
    Create test files for demonstration
    """
    # Create a normal text file
    write_file_safely("test_data.txt", "This is a test file with some sample data.\nLine 2 of the file.")
    
    # Create a file with special characters
    write_file_safely("special_chars.txt", "File with special characters: áéíóú ñ ¿¡")

# Test the enhanced functions
if __name__ == "__main__":
    print("=== Creating test files ===")
    create_test_files()
    
    print("\n=== Testing file reading ===")
    content = read_file_with_context_manager("test_data.txt")
    if content:
        print(f"File content preview: {content[:50]}...")
    
    print("\n=== Testing with non-existent file ===")
    read_file_with_context_manager("missing_file.txt")
    
    print("\n=== Testing special characters ===")
    read_file_with_context_manager("special_chars.txt")