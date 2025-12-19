import json
import sys

class JSONExplorer:
    def __init__(self, filename):
        self.data = self.load_data(filename)
        self.current_path = []
        self.current_data = self.data
    
    def load_data(self, filename):
        """Load JSON data from file"""
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading file: {e}")
            return None
    
    def display_current_level(self):
        """Display current level information"""
        path_str = " -> ".join(self.current_path) if self.current_path else "Root"
        print(f"\nCurrent Location: {path_str}")
        print("=" * 50)
        
        if isinstance(self.current_data, dict):
            print("Available keys:")
            for i, key in enumerate(self.current_data.keys(), 1):
                value_type = type(self.current_data[key]).__name__
                if isinstance(self.current_data[key], (dict, list)):
                    size = len(self.current_data[key])
                    print(f"  {i}. {key} ({value_type}, {size} items)")
                else:
                    preview = str(self.current_data[key])[:50]
                    print(f"  {i}. {key} ({value_type}): {preview}")
        
        elif isinstance(self.current_data, list):
            print(f"List with {len(self.current_data)} items:")
            for i, item in enumerate(self.current_data[:10]):  # Show first 10 items
                item_type = type(item).__name__
                if isinstance(item, dict) and item:
                    first_key = list(item.keys())[0]
                    print(f"  {i}. {item_type} (first key: {first_key})")
                else:
                    preview = str(item)[:50]
                    print(f"  {i}. {item_type}: {preview}")
            
            if len(self.current_data) > 10:
                print(f"  ... and {len(self.current_data) - 10} more items")
        
        else:
            print(f"Value: {self.current_data}")
    
    def navigate_to_key(self, key):
        """Navigate to a specific key"""
        if isinstance(self.current_data, dict) and key in self.current_data:
            self.current_path.append(key)
            self.current_data = self.current_data[key]
            return True
        return False
    
    def navigate_to_index(self, index):
        """Navigate to a specific list index"""
        if isinstance(self.current_data, list) and 0 <= index < len(self.current_data):
            self.current_path.append(f"[{index}]")
            self.current_data = self.current_data[index]
            return True
        return False
    
    def go_back(self):
        """Go back one level"""
        if self.current_path:
            self.current_path.pop()
            # Rebuild current_data by following the path
            self.current_data = self.data
            for step in self.current_path:
                if step.startswith('[') and step.endswith(']'):
                    # It's an index
                    index = int(step[1:-1])
                    self.current_data = self.current_data[index]
                else:
                    # It's a key
                    self.current_data = self.current_data[step]
            return True
        return False
    
    def search_current_level(self, term):
        """Search for a term in current level"""
        results = []
        
        if isinstance(self.current_data, dict):
            for key, value in self.current_data.items():
                if term.lower() in key.lower():
                    results.append(f"Key: {key}")
                if isinstance(value, str) and term.lower() in value.lower():
                    results.append(f"Value in {key}: {value}")
        
        elif isinstance(self.current_data, list):
            for i, item in enumerate(self.current_data):
                if isinstance(item, str) and term.lower() in item.lower():
                    results.append(f"Item {i}: {item}")
                elif isinstance(item, dict):
                    for key, value in item.items():
                        if isinstance(value, str) and term.lower() in value.lower():
                            results.append(f"Item {i}.{key}: {value}")
        
        return results
    
    def run(self):
        """Main interactive loop"""
        if not self.data:
            print("No data loaded. Exiting.")
            return
        
        print("JSON Explorer - Interactive Navigation")
        print("Commands: key_name, index, back, search <term>, quit")
        print("=" * 50)
        
        while True:
            self.display_current_level()
            
            command = input("\nEnter command: ").strip()
            
            if command.lower() == 'quit':
                print("Goodbye!")
                break
            
            elif command.lower() == 'back':
                if not self.go_back():
                    print("Already at root level.")
            
            elif command.lower().startswith('search '):
                search_term = command[7:]  # Remove 'search ' prefix
                results = self.search_current_level(search_term)
                if results:
                    print(f"\nSearch results for '{search_term}':")
                    for result in results:
                        print(f"  • {result}")
                else:
                    print(f"No results found for '{search_term}'")
            
            elif command.isdigit():
                index = int(command)
                if not self.navigate_to_index(index):
                    print(f"Invalid index: {index}")
            
            else:
                if not self.navigate_to_key(command):
                    print(f"Key '{command}' not found at current level.")

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Enter JSON filename: ").strip()
    
    explorer = JSONExplorer(filename)
    explorer.run()

if __name__ == "__main__":
    main()