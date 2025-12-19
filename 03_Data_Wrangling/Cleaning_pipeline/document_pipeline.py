def document_pipeline():
    """
    Generate documentation for the data cleaning pipeline
    """
    documentation = """
    ================================================================
    CUSTOM DATA CLEANING PIPELINE DOCUMENTATION
    ================================================================
    
    OVERVIEW:
    This pipeline provides a comprehensive solution for cleaning and 
    preprocessing datasets across different domains.
    
    MAIN FUNCTION:
    clean_data(df, dataset_type="general")
    
    PARAMETERS:
    - df: pandas DataFrame to be cleaned
    - dataset_type: string indicating the type of dataset
      Options: "general", "hospital", "transport"
    
    CLEANING STEPS:
    1. Handle Missing Values
       - Numeric: Fill with median
       - Categorical: Fill with mode or 'Unknown'
       - Datetime: Forward fill
    
    2. Remove Duplicates
       - Identifies and removes duplicate rows
    
    3. Fix Data Types
       - Converts string numbers to numeric
       - Handles datetime conversions
       - Dataset-specific type corrections
    
    4. Handle Outliers
       - Uses IQR method for detection
       - Caps outliers instead of removing
    
    5. Standardize Text Data
       - Removes extra whitespace
       - Applies consistent case formatting
       - Standardizes naming conventions
    
    USAGE EXAMPLES:
    
    # Basic usage
    cleaned_df = clean_data(raw_df, "general")
    
    # Hospital-specific cleaning
    hospital_clean = clean_data(hospital_df, "hospital")
    
    # Complete pipeline with reporting
    results = complete_data_cleaning_pipeline(df, "transport", save_results=True)
    
    BEST PRACTICES:
    1. Always backup original data before cleaning
    2. Validate results after cleaning
    3. Document any custom cleaning rules
    4. Test pipeline with sample data first
    5. Monitor performance with large datasets
    
    ================================================================
    """
    
    print(documentation)
    
    # Save documentation to file
    with open('pipeline_documentation.txt', 'w') as f:
        f.write(documentation)
    
    print("✓ Documentation saved to 'pipeline_documentation.txt'")
