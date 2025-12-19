import json

def load_json_data(filename):
    """
    Load JSON data from file
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}")
        return None

def extract_basic_info(data):
    """
    Extract basic company information
    """
    company = data['company']
    print("BASIC COMPANY INFORMATION:")
    print("=" * 40)
    print(f"Company Name: {company['name']}")
    print(f"Founded: {company['founded']}")
    
    # Navigate nested address structure
    hq = company['headquarters']
    address = hq['address']
    print(f"Headquarters: {address['street']}, {address['city']}, {address['state']}")
    print(f"Coordinates: {hq['coordinates']['latitude']}, {hq['coordinates']['longitude']}")

def analyze_departments(data):
    """
    Analyze department structure and information
    """
    departments = data['company']['departments']
    
    print("\nDEPARTMENT ANALYSIS:")
    print("=" * 40)
    
    for dept_name, dept_info in departments.items():
        print(f"\n{dept_name.upper()} Department:")
        print(f"  Head: {dept_info['head']}")
        print(f"  Budget: ${dept_info['budget']:,}")
        
        # Handle different department structures
        if 'teams' in dept_info:
            print("  Teams:")
            for team_name, team_info in dept_info['teams'].items():
                print(f"    • {team_name.title()} Team (Lead: {team_info['lead']})")
                print(f"      Members: {len(team_info['members'])}")
                print(f"      Technologies: {', '.join(team_info['technologies'])}")
        
        elif 'campaigns' in dept_info:
            print("  Campaigns:")
            for campaign in dept_info['campaigns']:
                print(f"    • {campaign['name']}")
                print(f"      Budget: ${campaign['budget']:,}")
                print(f"      Channels: {', '.join(campaign['channels'])}")

def extract_team_members(data):
    """
    Extract and display all team members with their details
    """
    print("\nTEAM MEMBERS DIRECTORY:")
    print("=" * 40)
    
    engineering = data['company']['departments']['engineering']
    
    for team_name, team_info in engineering['teams'].items():
        print(f"\n{team_name.upper()} TEAM:")
        print(f"Team Lead: {team_info['lead']}")
        print("Members:")
        
        for member in team_info['members']:
            print(f"  • {member['name']} - {member['role']} ({member['experience']} years)")

def analyze_financial_data(data):
    """
    Analyze financial information
    """
    financial = data['company']['financial']
    
    print("\nFINANCIAL ANALYSIS:")
    print("=" * 40)
    
    # Revenue analysis
    revenue = financial['revenue']
    print("Revenue Trend:")
    for year, amount in revenue.items():
        print(f"  {year}: ${amount:,}")
    
    # Calculate growth rate
    growth_2023 = ((revenue['2023'] - revenue['2022']) / revenue['2022']) * 100
    print(f"  Growth 2022-2023: {growth_2023:.1f}%")
    
    # Expense breakdown for 2023
    expenses_2023 = financial['expenses']['2023']
    total_expenses = sum(expenses_2023.values())
    
    print(f"\n2023 Expenses (Total: ${total_expenses:,}):")
    for category, amount in expenses_2023.items():
        percentage = (amount / total_expenses) * 100
        print(f"  {category.title()}: ${amount:,} ({percentage:.1f}%)")

def search_nested_data(data, search_term):
    """
    Search for a specific term in nested JSON structure
    """
    def search_recursive(obj, path=""):
        results = []
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                current_path = f"{path}.{key}" if path else key
                
                # Check if search term is in key or value
                if search_term.lower() in str(key).lower():
                    results.append(f"Key found at: {current_path}")
                
                if isinstance(value, str) and search_term.lower() in value.lower():
                    results.append(f"Value found at: {current_path} = '{value}'")
                
                # Recursively search nested structures
                results.extend(search_recursive(value, current_path))
        
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                current_path = f"{path}[{i}]"
                results.extend(search_recursive(item, current_path))
        
        return results
    
    print(f"\nSEARCH RESULTS for '{search_term}':")
    print("=" * 40)
    results = search_recursive(data)
    
    if results:
        for result in results:
            print(f"  • {result}")
    else:
        print(f"  No results found for '{search_term}'")

def main():
    # Load the nested JSON data
    filename = "company_data.json"
    data = load_json_data(filename)
    
    if not data:
        return
    
    # Extract basic information
    extract_basic_info(data)
    
    # Analyze departments
    analyze_departments(data)
    
    # Extract team members
    extract_team_members(data)
    
    # Analyze financial data
    analyze_financial_data(data)
    
    # Demonstrate search functionality
    search_nested_data(data, "Python")
    search_nested_data(data, "Sarah")

if __name__ == "__main__":
    main()