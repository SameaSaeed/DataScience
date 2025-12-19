import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('default')
sns.set_palette("husl")

class TransactionAnomalyDetector:
    def __init__(self, csv_file):
        """Initialize the detector with transaction data"""
        self.df = None
        self.load_data(csv_file)
        
    def load_data(self, csv_file):
        """Load transaction data from CSV file"""
        try:
            print(f"Loading transaction data from {csv_file}...")
            self.df = pd.read_csv(csv_file)
            
            # Convert timestamp to datetime
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            
            print(f"Successfully loaded {len(self.df)} transactions")
            print(f"Columns: {list(self.df.columns)}")
            print("\nData types:")
            print(self.df.dtypes)
            
        except FileNotFoundError:
            print(f"Error: File {csv_file} not found!")
            return False
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
            
        return True
    
    def explore_data(self):
        """Explore the basic statistics of the transaction data"""
        print("\n" + "="*50)
        print("TRANSACTION DATA EXPLORATION")
        print("="*50)
        
        # Basic statistics
        print("\nBasic Statistics:")
        print(f"Total transactions: {len(self.df)}")
        print(f"Date range: {self.df['timestamp'].min()} to {self.df['timestamp'].max()}")
        print(f"Unique users: {self.df['user_id'].nunique()}")
        print(f"Transaction types: {self.df['transaction_type'].unique()}")
        
        # Amount statistics
        print(f"\nAmount Statistics:")
        print(f"Mean amount: ${self.df['amount'].mean():.2f}")
        print(f"Median amount: ${self.df['amount'].median():.2f}")
        print(f"Min amount: ${self.df['amount'].min():.2f}")
        print(f"Max amount: ${self.df['amount'].max():.2f}")
        print(f"Standard deviation: ${self.df['amount'].std():.2f}")
        
        # Display first few rows
        print(f"\nFirst 5 transactions:")
        print(self.df.head())
        
        return self.df.describe()
    
    def calculate_iqr_anomalies(self, column='amount', multiplier=1.5):
        """
        Calculate IQR-based anomalies for a numeric column
        
        Parameters:
        - column: The column to analyze (default: 'amount')
        - multiplier: IQR multiplier for outlier detection (default: 1.5)
        """
        print(f"\n" + "="*50)
        print(f"IQR ANOMALY DETECTION FOR {column.upper()}")
        print("="*50)
        
        # Calculate quartiles
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        # Calculate bounds
        lower_bound = Q1 - (multiplier * IQR)
        upper_bound = Q3 + (multiplier * IQR)
        
        print(f"Q1 (25th percentile): ${Q1:.2f}")
        print(f"Q3 (75th percentile): ${Q3:.2f}")
        print(f"IQR: ${IQR:.2f}")
        print(f"Lower bound: ${lower_bound:.2f}")
        print(f"Upper bound: ${upper_bound:.2f}")
        
        # Identify anomalies
        anomalies = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
        
        # Add anomaly flags to the main dataframe
        self.df['iqr_anomaly'] = ((self.df[column] < lower_bound) | (self.df[column] > upper_bound))
        
        print(f"\nAnomalies found: {len(anomalies)} ({len(anomalies)/len(self.df)*100:.2f}%)")
        
        if len(anomalies) > 0:
            print(f"\nTop 10 IQR anomalies:")
            print(anomalies.nlargest(10, column)[['transaction_id', 'user_id', column, 'merchant_category']])
        
        # Create visualization
        self.visualize_iqr_anomalies(column, Q1, Q3, lower_bound, upper_bound)
        
        return anomalies
    
    def visualize_iqr_anomalies(self, column, Q1, Q3, lower_bound, upper_bound):
        """Create visualizations for IQR anomalies"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Box plot
        ax1.boxplot(self.df[column], vert=True)
        ax1.set_ylabel(f'{column.title()} ($)')
        ax1.set_title(f'Box Plot of {column.title()}')
        ax1.grid(True, alpha=0.3)
        
        # Histogram with anomaly boundaries
        ax2.hist(self.df[column], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        ax2.axvline(lower_bound, color='red', linestyle='--', label=f'Lower bound: ${lower_bound:.2f}')
        ax2.axvline(upper_bound, color='red', linestyle='--', label=f'Upper bound: ${upper_bound:.2f}')
        ax2.axvline(Q1, color='orange', linestyle='-', label=f'Q1: ${Q1:.2f}')
        ax2.axvline(Q3, color='orange', linestyle='-', label=f'Q3: ${Q3:.2f}')
        ax2.set_xlabel(f'{column.title()} ($)')
        ax2.set_ylabel('Frequency')
        ax2.set_title(f'Distribution of {column.title()} with IQR Bounds')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'iqr_anomalies_{column}.png', dpi=300, bbox_inches='tight')
        plt.show()
        print(f"Visualization saved as 'iqr_anomalies_{column}.png'")
    def calculate_zscore_anomalies(self, column='amount', threshold=2.5):
        """
        Calculate Z-score based anomalies for a numeric column
        
        Parameters:
        - column: The column to analyze (default: 'amount')
        - threshold: Z-score threshold for anomaly detection (default: 2.5)
        """
        print(f"\n" + "="*50)
        print(f"Z-SCORE ANOMALY DETECTION FOR {column.upper()}")
        print("="*50)
        
        # Calculate mean and standard deviation
        mean_val = self.df[column].mean()
        std_val = self.df[column].std()
        
        print(f"Mean: ${mean_val:.2f}")
        print(f"Standard deviation: ${std_val:.2f}")
        print(f"Z-score threshold: ±{threshold}")
        
        # Calculate z-scores
        self.df[f'{column}_zscore'] = np.abs((self.df[column] - mean_val) / std_val)
        
        # Identify anomalies
        anomalies = self.df[self.df[f'{column}_zscore'] > threshold]
        
        # Add anomaly flags
        self.df['zscore_anomaly'] = self.df[f'{column}_zscore'] > threshold
        
        print(f"\nAnomalies found: {len(anomalies)} ({len(anomalies)/len(self.df)*100:.2f}%)")
        
        if len(anomalies) > 0:
            print(f"\nTop 10 Z-score anomalies:")
            anomaly_display = anomalies.nlargest(10, f'{column}_zscore')[
                ['transaction_id', 'user_id', column, f'{column}_zscore', 'merchant_category']
            ]
            print(anomaly_display)
        
        # Create visualization
        self.visualize_zscore_anomalies(column, threshold)
        
        return anomalies
    
    def visualize_zscore_anomalies(self, column, threshold):
        """Create visualizations for Z-score anomalies"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Scatter plot of values vs z-scores
        normal_data = self.df[self.df[f'{column}_zscore'] <= threshold]
        anomaly_data = self.df[self.df[f'{column}_zscore'] > threshold]
        
        ax1.scatter(normal_data.index, normal_data[column], alpha=0.6, color='blue', label='Normal', s=20)
        ax1.scatter(anomaly_data.index, anomaly_data[column], alpha=0.8, color='red', label='Anomaly', s=30)
        ax1.set_xlabel('Transaction Index')
        ax1.set_ylabel(f'{column.title()} ($)')
        ax1.set_title(f'{column.title()} Values with Z-score Anomalies')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Z-score distribution
        ax2.hist(self.df[f'{column}_zscore'], bins=50, alpha=0.7, color='lightgreen', edgecolor='black')
        ax2.axvline(threshold, color='red', linestyle='--', label=f'Threshold: {threshold}')
        ax2.set_xlabel('Z-score')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Distribution of Z-scores')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'zscore_anomalies_{column}.png', dpi=300, bbox_inches='tight')
        plt.show()
        print(f"Visualization saved as 'zscore_anomalies_{column}.png'")
    def flag_high_risk_transactions(self, amount_threshold=1000, zscore_threshold=2.0, 
                                  iqr_multiplier=1.5, combine_methods=True):
        """
        Flag high-risk transactions based on multiple criteria
        
        Parameters:
        - amount_threshold: Direct amount threshold for high-risk flagging
        - zscore_threshold: Z-score threshold
        - iqr_multiplier: IQR multiplier
        - combine_methods: Whether to combine multiple detection methods
        """
        print(f"\n" + "="*60)
        print("HIGH-RISK TRANSACTION FLAGGING")
        print("="*60)
        
        # Initialize risk flags
        self.df['high_amount_risk'] = self.df['amount'] > amount_threshold
        
        # Ensure anomaly columns exist
        if 'iqr_anomaly' not in self.df.columns:
            self.calculate_iqr_anomalies('amount', iqr_multiplier)
        if 'zscore_anomaly' not in self.df.columns:
            self.calculate_zscore_anomalies('amount', zscore_threshold)
        
        # Create combined risk score
        if combine_methods:
            self.df['risk_score'] = (
                self.df['high_amount_risk'].astype(int) +
                self.df['iqr_anomaly'].astype(int) +
                self.df['zscore_anomaly'].astype(int)
            )
            
            # Flag as high-risk if any method detects anomaly
            self.df['high_risk'] = (
                self.df['high_amount_risk'] |
                self.df['iqr_anomaly'] |
                self.df['zscore_anomaly']
            )
        else:
            self.df['risk_score'] = self.df['high_amount_risk'].astype(int)
            self.df['high_risk'] = self.df['high_amount_risk']
        
        # Calculate statistics
        high_risk_count = self.df['high_risk'].sum()
        high_risk_percentage = (high_risk_count / len(self.df)) * 100
        
        print(f"Risk Assessment Results:")
        print(f"- High amount (>${amount_threshold}): {self.df['high_amount_risk'].sum()} transactions")
        print(f"- IQR anomalies: {self.df['iqr_anomaly'].sum()} transactions")
        print(f"- Z-score anomalies: {self.df['zscore_anomaly'].sum()} transactions")
        print(f"- Total high-risk transactions: {high_risk_count} ({high_risk_percentage:.2f}%)")
        
        # Show high-risk transactions
        high_risk_transactions = self.df[self.df['high_risk']].copy()
        
        if len(high_risk_transactions) > 0:
            print(f"\nTop 15 High-Risk Transactions:")
            display_cols = ['transaction_id', 'user_id', 'amount', 'merchant_category', 
                          'risk_score', 'high_amount_risk', 'iqr_anomaly', 'zscore_anomaly']
            print(high_risk_transactions.nlargest(15, 'amount')[display_cols])
            
            # Risk distribution by category
            print(f"\nRisk Distribution by Merchant Category:")
            risk_by_category = high_risk_transactions.groupby('merchant_category').agg({
                'transaction_id': 'count',
                'amount': ['mean', 'max']
            }).round(2)
            print(risk_by_category)
        
        # Create comprehensive visualization
        self.visualize_risk_assessment()
        
        return high_risk_transactions
    
    def visualize_risk_assessment(self):
        """Create comprehensive risk assessment visualizations"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Risk score distribution
        risk_counts = self.df['risk_score'].value_counts().sort_index()
        ax1.bar(risk_counts.index, risk_counts.values, color=['green', 'yellow', 'orange', 'red'][:len(risk_counts)])
        ax1.set_xlabel('Risk Score')
        ax1.set_ylabel('Number of Transactions')
        ax1.set_title('Distribution of Risk Scores')
        ax1.grid(True, alpha=0.3)
        
        # Amount distribution by risk level
        high_risk_amounts = self.df[self.df['high_risk']]['amount']
        normal_amounts = self.df[~self.df['high_risk']]['amount']
        
        ax2.hist([normal_amounts, high_risk_amounts], bins=50, alpha=0.7, 
                label=['Normal', 'High Risk'], color=['blue', 'red'])
        ax2.set_xlabel('Transaction Amount ($)')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Amount Distribution: Normal vs High Risk')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Risk by merchant category
        risk_by_merchant = self.df.groupby('merchant_category')['high_risk'].agg(['count', 'sum'])
        risk_by_merchant['risk_rate'] = (risk_by_merchant['sum'] / risk_by_merchant['count'] * 100)
        
        ax3.bar(risk_by_merchant.index, risk_by_merchant['risk_rate'], color='coral')
        ax3.set_xlabel('Merchant Category')
        ax3.set_ylabel('Risk Rate (%)')
        ax3.set_title('Risk Rate by Merchant Category')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)
        
        # Timeline of high-risk transactions
        high_risk_timeline = self.df[self.df['high_risk']].copy()
        if len(high_risk_timeline) > 0:
            high_risk_timeline['date'] = high_risk_timeline['timestamp'].dt.date
            daily_risk = high_risk_timeline.groupby('date').size()
            
            ax4.plot(daily_risk.index, daily_risk.values, marker='o', color='red', linewidth=2)
            ax4.set_xlabel('Date')
            ax4.set_ylabel('High-Risk Transactions')
            ax4.set_title('High-Risk Transactions Over Time')
            ax4.tick_params(axis='x', rotation=45)
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('risk_assessment_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("Risk assessment dashboard saved as 'risk_assessment_dashboard.png'")
    def generate_summary_report(self):
        """Generate a comprehensive summary report"""
        print(f"\n" + "="*60)
        print("ANOMALY DETECTION SUMMARY REPORT")
        print("="*60)
        
        total_transactions = len(self.df)
        high_risk_count = self.df['high_risk'].sum() if 'high_risk' in self.df.columns else 0
        
        print(f"Dataset Overview:")
        print(f"- Total transactions analyzed: {total_transactions:,}")
        print(f"- Date range: {self.df['timestamp'].min().strftime('%Y-%m-%d')} to {self.df['timestamp'].max().strftime('%Y-%m-%d')}")
        print(f"- Unique users: {self.df['user_id'].nunique():,}")
        
        print(f"\nAnomaly Detection Results:")
        if 'iqr_anomaly' in self.df.columns:
            iqr_anomalies = self.df['iqr_anomaly'].sum()
            print(f"- IQR method detected: {iqr_anomalies:,} anomalies ({iqr_anomalies/total_transactions*100:.2f}%)")
        
        if 'zscore_anomaly' in self.df.columns:
            zscore_anomalies = self.df['zscore_anomaly'].sum()
            print(f"- Z-score method detected: {zscore_anomalies:,} anomalies ({zscore_anomalies/total_transactions*100:.2f}%)")
        
        if 'high_amount_risk' in self.df.columns:
            high_amount_count = self.df['high_amount_risk'].sum()
            print(f"- High amount threshold detected: {high_amount_count:,} transactions")
        
        print(f"- Combined high-risk transactions: {high_risk_count:,} ({high_risk_count/total_transactions*100:.2f}%)")
        
        if high_risk_count > 0:
            high_risk_data = self.df[self.df['high_risk']]
            print(f"\nHigh-Risk Transaction Analysis:")
            print(f"- Average high-risk amount: ${high_risk_data['amount'].mean():.2f}")
            print(f"- Maximum high-risk amount: ${high_risk_data['amount'].max():.2f}")
            print(f"- Most common high-risk category: {high_risk_data['merchant_category'].mode().iloc[0]}")
        
        print(f"\nRecommendations:")
        print(f"- Review all {high_risk_count} high-risk transactions manually")
        print(f"- Implement real-time monitoring for amounts > ${self.df['amount'].quantile(0.95):.2f}")
        print(f"- Consider additional verification for transactions with risk_score >= 2")
        
        # Save detailed report to file
        self.save_detailed_report()
    
    def save_detailed_report(self):
        """Save detailed anomaly report to CSV"""
        if 'high_risk' in self.df.columns:
            # Save all transactions with risk indicators
            report_df = self.df.copy()
            report_df.to_csv('anomaly_detection_report.csv', index=False)
            
            # Save only high-risk transactions
            high_risk_df = self.df[self.df['high_risk']].copy()
            high_risk_df.to_csv('high_risk_transactions.csv', index=False)
            
            print(f"\nReports saved:")
            print(f"- Complete report: anomaly_detection_report.csv")
            print(f"- High-risk transactions only: high_risk_transactions.csv")

# Initialize the detector
detector = TransactionAnomalyDetector('transaction_logs.csv')

# Explore the data
stats_summary = detector.explore_data()
print(f"\nDetailed Statistics Summary:")
print(stats_summary)

# Calculate IQR anomalies
iqr_anomalies = detector.calculate_iqr_anomalies('amount')

zscore_anomalies = detector.calculate_zscore_anomalies('amount', threshold=2.0)

# Flag high-risk transactions
high_risk_transactions = detector.flag_high_risk_transactions(
    amount_threshold=500,  # Lower threshold to catch more anomalies
    zscore_threshold=2.0,
    iqr_multiplier=1.5,
    combine_methods=True
)

# Generate summary report
detector.generate_summary_report()

print(f"\n" + "="*60)
print("="*60)
print("Check the generated files:")
print("- transaction_logs.csv (original data)")
print("- anomaly_detection_report.csv (complete analysis)")
print("- high_risk_transactions.csv (flagged transactions)")
print("- Various PNG visualization files")

# ls -la *.csv *.png
# head -10 high_risk_transactions.csv
# wc -l high_risk_transactions.csv