# Process data in chunks for large datasets
def clean_large_dataset(file_path, dataset_type, chunk_size=10000):
    """
    Clean large datasets by processing in chunks
    """
    cleaned_chunks = []
    
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        cleaned_chunk = clean_data(chunk, dataset_type)
        cleaned_chunks.append(cleaned_chunk)
    
    return pd.concat(cleaned_chunks, ignore_index=True)