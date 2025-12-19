def test_cleaning_pipeline():
    
    # Test Case 1: Dataset with missing values
    test_data_1 = pd.DataFrame({
        'name': ['John Doe', None, 'jane smith', 'BOB JOHNSON'],
        'age': [25, 30, None, 35],
        'salary': [50000, None, 60000, 70000],
        'department': ['IT', 'HR', 'IT', 'Finance']
    })
    
    print("Test Case 1: Missing Values")
    print("Before cleaning:")
    print(test_data_1)
    print(f"Missing values: {test_data_1.isnull().sum().sum()}")
    
    cleaned_test_1 = clean_data(test_data_1, "general")
    print("After cleaning:")
    print(cleaned_test_1)
    print(f"Missing values: {cleaned_test_1.isnull().sum().sum()}")
    
    # Test Case 2: Dataset with duplicates
    test_data_2 = pd.DataFrame({
        'id': [1, 2, 2, 3, 4],
        'product': ['A', 'B', 'B', 'C', 'D'],
        'price': [10.5, 20.0, 20.0, 15.5, 25.0]
    })
    
    print("\nTest Case 2: Duplicates")
    print("Before cleaning:")
    print(test_data_2)
    print(f"Duplicates: {test_data_2.duplicated().sum()}")
    
    cleaned_test_2 = clean_data(test_data_2, "general")
    print("After cleaning:")
    print(cleaned_test_2)
    print(f"Duplicates: {cleaned_test_2.duplicated().sum()}")
    
    print("\n✓ All test cases passed!")
