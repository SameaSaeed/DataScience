import json
import os
from datetime import datetime

# Custom Exception Classes
class JSONFileError(Exception):
    """Base exception for JSON file operations"""
    pass

class JSONValidationError(JSONFileError):
    """Exception raised when JSON data validation fails"""
    pass

class JSONStructureError(JSONFileError):
    """Exception raised when JSON structure is invalid"""
    pass

class JSONProcessor:
    """
    Advanced JSON processor with custom exception handling
    """
    
    def __init__(self):
        self.processed_files = []
    
    def load_json_with_validation(self, filename, schema=None):
        """
        Load JSON file with optional schema validation
        """
        try:
            # Check if file exists
            if not os.path.exists(filename):
                raise FileNotFoundError(f"JSON file '{filename}' does not exist")
            
            # Read and parse JSON
            with open(filename, 'r') as file:
                data = json.load(file)
            
            # Validate against schema if provided
            if schema:
                self._validate_schema(data, schema, filename)
            
            # Track processed files
            self.processed_files.append({
                'filename': filename,
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            })
            
            print(f"Successfully loaded and validated JSON from '{filename}'")
            return data
        
        except FileNotFoundError as e:
            self._log_error(filename, 'file_not_found', str(e))
            raise JSONFileError(f"File error: {e}")
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in '{filename}' at line {e.lineno}, column {e.colno}: {e.msg}"
            self._log_error(filename, 'json_decode_error', error_msg)
            raise JSONFileError(error_msg)
        
        except JSONValidationError as e:
            self._log_error(filename, 'validation_error', str(e))
            raise
        
        except Exception as e:
            error_msg = f"Unexpected error processing '{filename}': {type(e).__name__}: {e}"
            self._log_error(filename, 'unexpected_error', error_msg)
            raise JSONFileError(error_msg)
    
    def _validate_schema(self, data, schema, filename):
        """
        Validate JSON data against a simple schema
        """
        try:
            # Check if data is a dictionary
            if not isinstance(data, dict):
                raise JSONStructureError(f"Expected dictionary, got {type(data).__name__}")
            
            # Check required fields
            if 'required_fields' in schema:
                missing_fields = []
                for field in schema['required_fields']:
                    if field not in data:
                        missing_fields.append(field)
                
                if missing_fields:
                    raise JSONValidationError(f"Missing required fields in '{filename}': {missing_fields}")
            
            # Check field types
            if 'field_types' in schema:
                for field, expected_type in schema['field_types'].items():
                    if field in data:
                        if not isinstance(data[field], expected_type):
                            raise JSONValidationError(
                                f"Field '{field}' in '{filename}' should be {expected_type.__name__}, "
                                f"got {type(data[field]).__name__}"
                            )
            
            print(f"Schema validation passed for '{filename}'")
        
        except (JSONStructureError, JSONValidationError):
            raise
        
        except Exception as e:
            raise JSONValidationError(f"Schema validation error: {e}")
    
    def _log_error(self, filename, error_type, message):
        """
        Log error information
        """
        self.processed_files.append({
            'filename': filename,
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error_type': error_type,
            'message': message
        })
    
    def get_processing_summary(self):
        """
        Get summary of processed files
        """
        total_files = len(self.processed_files)
        successful = len([f for f in self.processed_files if f['status'] == 'success'])
        failed = total_files - successful
        
        return {
            'total_processed': total_files,
            'successful': successful,
            'failed': failed,
            'details': self.processed_files
        }

def create_test_files_for_advanced_processing():
    """
    Create various test files for advanced processing
    """
    # Valid user data
    user_data = {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "age": 28,
        "active": True,
        "roles": ["user", "admin"]
    }
    
    # Invalid user data (missing required field)
    invalid_user_data = {
        "name": "Bob Smith",
        "age": 35,
        "active": True
        # Missing email field
    }
    
    # User data with wrong types
    wrong_type_data = {
        "id": "should_be_number",  # Wrong type
        "name": "Charlie Brown",
        "email": "charlie@example.com",
        "age": "thirty",  # Wrong type
        "active": True
    }
    
    # Write test files
    with open("valid_user.json", 'w') as f:
        json.dump(user_data, f, indent=2)
    
    with open("invalid_user.json", 'w') as f:
        json.dump(invalid_user_data, f, indent=2)
    
    with open("wrong_types.json", 'w') as f:
        json.dump(wrong_type_data, f, indent=2)
    
    print("Created test files for advanced processing")

# Test the advanced JSON processor
if __name__ == "__main__":
    print("=== Creating test files ===")
    create_test_files_for_advanced_processing()
    
    # Define schema for validation
    user_schema = {
        'required_fields': ['id', 'name', 'email', 'age'],
        'field_types': {
            'id': int,
            'name': str,
            'email': str,
            'age': int,
            'active': bool
        }
    }
    
    processor = JSONProcessor()
    
    print("\n=== Testing valid JSON file ===")
    try:
        data = processor.load_json_with_validation("valid_user.json", user_schema)
        print(f"Loaded data: {data}")
    except JSONFileError as e:
        print(f"JSON File Error: {e}")
    
    print("\n=== Testing invalid JSON file (missing field) ===")
    try:
        data = processor.load_json_with_validation("invalid_user.json", user_schema)
    except JSONFileError as e:
        print(f"JSON File Error: {e}")
    
    print("\n=== Testing JSON file with wrong types ===")
    try:
        data = processor.load_json_with_validation("wrong_types.json", user_schema)
    except JSONFileError as e:
        print(f"JSON File Error: {e}")
    
    print("\n=== Testing non-existent file ===")
    try:
        data = processor.load_json_with_validation("nonexistent.json", user_schema)
    except JSONFileError as e:
        print(f"JSON File Error: {e}")
    
    print("\n=== Processing Summary ===")
    summary = processor.get_processing_summary()
    print(f"Total files processed: {summary['total_processed']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")