import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate sample transaction data
def generate_transaction_data(num_transactions=1000):
    # Create base data
    data = []
    
    # Normal transaction patterns
    for i in range(int(num_transactions * 0.95)):  # 95% normal transactions
        transaction = {
            'transaction_id': f'TXN_{i+1:06d}',
            'user_id': f'USER_{random.randint(1, 200):04d}',
            'amount': round(np.random.normal(150, 75), 2),  # Normal distribution around $150
            'timestamp': datetime.now() - timedelta(days=random.randint(0, 30)),
            'merchant_category': random.choice(['grocery', 'gas', 'restaurant', 'retail', 'online']),
            'location': random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
            'transaction_type': random.choice(['purchase', 'withdrawal', 'transfer'])
        }
        
        # Ensure positive amounts for purchases
        if transaction['amount'] < 0:
            transaction['amount'] = abs(transaction['amount'])
            
        data.append(transaction)
    
    # Add anomalous transactions (5%)
    for i in range(int(num_transactions * 0.05)):
        anomaly_type = random.choice(['high_amount', 'unusual_time', 'frequent_transactions'])
        
        if anomaly_type == 'high_amount':
            transaction = {
                'transaction_id': f'TXN_{len(data)+1:06d}',
                'user_id': f'USER_{random.randint(1, 200):04d}',
                'amount': round(np.random.uniform(2000, 10000), 2),  # Unusually high amounts
                'timestamp': datetime.now() - timedelta(days=random.randint(0, 30)),
                'merchant_category': random.choice(['jewelry', 'electronics', 'luxury']),
                'location': random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
                'transaction_type': 'purchase'
            }
        else:
            transaction = {
                'transaction_id': f'TXN_{len(data)+1:06d}',
                'user_id': f'USER_{random.randint(1, 200):04d}',
                'amount': round(np.random.normal(150, 75), 2),
                'timestamp': datetime.now() - timedelta(days=random.randint(0, 30)),
                'merchant_category': random.choice(['grocery', 'gas', 'restaurant', 'retail', 'online']),
                'location': random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
                'transaction_type': random.choice(['purchase', 'withdrawal', 'transfer'])
            }
            
        if transaction['amount'] < 0:
            transaction['amount'] = abs(transaction['amount'])
            
        data.append(transaction)
    
    return data

# Generate the data
print("Generating transaction data...")
transactions = generate_transaction_data(1000)

# Convert to DataFrame
df = pd.DataFrame(transactions)

# Save to CSV
df.to_csv('transaction_logs.csv', index=False)
print(f"Generated {len(df)} transactions and saved to 'transaction_logs.csv'")
print("\nFirst 5 transactions:")
print(df.head())