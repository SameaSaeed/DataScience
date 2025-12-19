def safe_type_conversion(series, target_type):
    """
    Safely convert series to target type with error handling
    """
    try:
        if target_type == 'numeric':
            return pd.to_numeric(series, errors='coerce')
        elif target_type == 'datetime':
            return pd.to_datetime(series, errors='coerce')
        else:
            return series.astype(target_type)
    except Exception as e:
        print(f"Type conversion failed: {e}")
        return series