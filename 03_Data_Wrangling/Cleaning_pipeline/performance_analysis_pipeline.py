import time

def analyze_pipeline_performance():
    """
    Analyze the performance of the cleaning pipeline
    """
    print("PIPELINE PERFORMANCE ANALYSIS")
    print("="*40)
    
    # Test with hospital data
    start_time = time.time()
    hospital_results = complete_data_cleaning_pipeline(hospital_data, "hospital")
    hospital_time = time.time() - start_time
    
    # Test with transport data
    start_time = time.time()
    transport_results = complete_data_cleaning_pipeline(transport_data, "transport")
    transport_time = time.time() - start_time
    
    print(f"Hospital dataset cleaning time: {hospital_time:.2f} seconds")
    print(f"Transport dataset cleaning time: {transport_time:.2f} seconds")
    
    # Calculate efficiency metrics
    hospital_rows_per_second = len(hospital_data) / hospital_time
    transport_rows_per_second = len(transport_data) / transport_time
    
    print(f"Hospital processing rate: {hospital_rows_per_second:.0f} rows/second")
    print(f"Transport processing rate: {transport_rows_per_second:.0f} rows/second")
    
    print("\n✓ Performance analysis completed!")