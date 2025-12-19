import pandas as pd

print("VALIDATION REPORT")
print("="*40)

# Load the results
try:
    original_data = pd.read_csv('transaction_logs.csv')
    analysis_report = pd.read_csv('anomaly_detection_report.csv')
    high_risk_data = pd.read_csv('high_risk_transactions.csv')
    
    print(f"Original transactions: {len(original_data):,}")
    print(f"Analysis report entries: {len(analysis_report):,}")
    print(f"High-risk transactions: {len(high_risk_data):,}")
    
    # Validate high-risk percentage
    risk_percentage = (len(high_risk_data) / len(original_data)) * 100
    print(f"High-risk percentage: {risk_percentage:.2f}%")
    
    # Show amount statistics for high-risk transactions
    if len(high_risk_data) > 0:
        print(f"\nHigh-risk transaction amounts:")
        print(f"- Mean: ${high_risk_data['amount'].mean()}")

except FileNotFoundError as e:
    print(f"Error: One of the CSV files is missing. {e}")
except pd.errors.EmptyDataError as e:
    print(f"Error: One of the CSV files is empty. {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")