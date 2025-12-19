def advanced_text_cleaning(series):
    """
    Advanced text cleaning for complex string data
    """
    # Remove special characters
    series = series.str.replace(r'[^\w\s]', '', regex=True)
    
    # Normalize whitespace
    series = series.str.replace(r'\s+', ' ', regex=True)
    
    # Handle common abbreviations
    abbreviations = {
        'St.': 'Street',
        'Ave.': 'Avenue',
        'Dr.': 'Doctor'
    }
    
    for abbrev, full in abbreviations.items():
        series = series.str.replace(abbrev, full)
    
    return series