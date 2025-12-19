#!/usr/bin/env python3
import csv
from collections import defaultdict
from datetime import datetime

def process_sales_and_create_summary(input_filename, output_filename):
    """
    Process sales data and create summary CSV report
    """
    sales_data = []
    
    # Read input CSV file
    try:
        with open(input_filename, 'r', newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            
            for row in csv_reader:
                quantity = int(row['Quantity'])
                price = float(row['Price'])
                total = quantity * price
                
                sale_record = {
                    'date': row['Date'],
                    'product': row['Product'],
                    'category': row['Category'],
                    'quantity': quantity,
                    'price': price,
                    'total': total,
                    'sales_rep': row['Sales_Rep']
                }
                sales_data.append(sale_record)
                
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        return False
    except Exception as e:
        print(f"Error reading input file: {e}")
        return False
    
    if not sales_data:
        print("No data to process.")
        return False
    
    # Calculate statistics
    sales_by_rep = defaultdict(lambda: {'total_sales': 0, 'total_quantity': 0, 'num_transactions': 0})
    sales_by_product = defaultdict(lambda: {'total_sales': 0, 'total_quantity': 0, 'num_transactions': 0})
    
    for record in sales_data:
        rep = record['sales_rep']
        product = record['product']
        
        # Update representative statistics
        sales_by_rep[rep]['total_sales'] += record['total']
        sales_by_rep[rep]['total_quantity'] += record['quantity']
        sales_by_rep[rep]['num_transactions'] += 1
        
        # Update product statistics
        sales_by_product[product]['total_sales'] += record['total']
        sales_by_product[product]['total_quantity'] += record['quantity']
        sales_by_product[product]['num_transactions'] += 1
    
    # Write summary to CSV file
    try:
        with open(output_filename, 'w', newline='') as csvfile:
            fieldnames = ['Type', 'Name', 'Total_Sales', 'Total_Quantity', 'Num_Transactions', 'Avg_Sale_Amount']
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            csv_writer.writeheader()
            
            # Write sales representative summary
            for rep, stats in sales_by_rep.items():
                avg_sale = stats['total_sales'] / stats['num_transactions'] if stats['num_transactions'] > 0 else 0
                csv_writer.writerow({
                    'Type': 'Sales_Rep',
                    'Name': rep,
                    'Total_Sales': round(stats['total_sales'], 2),
                    'Total_Quantity': stats['total_quantity'],
                    'Num_Transactions': stats['num_transactions'],
                    'Avg_Sale_Amount': round(avg_sale, 2)
                })
            
            # Write product summary
            for product, stats in sales_by_product.items():
                avg_sale = stats['total_sales'] / stats['num_transactions'] if stats['num_transactions'] > 0 else 0
                csv_writer.writerow({
                    'Type': 'Product',
                    'Name': product,
                    'Total_Sales': round(stats['total_sales'], 2),
                    'Total_Quantity': stats['total_quantity'],
                    'Num_Transactions': stats['num_transactions'],
                    'Avg_Sale_Amount': round(avg_sale, 2)
                })
        
        print(f"Summary report successfully written to '{output_filename}'")
        return True
        
    except Exception as e:
        print(f"Error writing summary file: {e}")
        return False

def create_detailed_report(input_filename, detailed_output_filename):
    """
    Create a detailed report with enhanced sales data
    """
    try:
        with open(input_filename, 'r', newline='') as input_file, \
             open(detailed_output_filename, 'w', newline='') as output_file:
            
            csv_reader = csv.DictReader(input_file)
            
            # Define output fieldnames (original + calculated fields)
            output_fieldnames = ['Date', 'Product', 'Category', 'Quantity', 'Price', 
                               'Total_Amount', 'Sales_Rep', 'Month', 'Day_of_Week']
            
            csv_writer = csv.DictWriter(output_file, fieldnames=output_fieldnames)
            csv_writer.writeheader()
            
            for row in csv_reader:
                quantity = int(row['Quantity'])
                price = float(row['Price'])
                total_amount = quantity * price
                
                # Parse date for additional information
                try:
                    date_obj = datetime.strptime(row['Date'], '%Y-%m-%d')
                    month = date_obj.strftime('%B')
                    day_of_week = date_obj.strftime('%A')
                except:
                    month = 'Unknown'
                    day_of_week = 'Unknown'
                
                # Write enhanced record
                csv_writer.writerow({
                    'Date': row['Date'],
                    'Product': row['Product'],
                    'Category': row['Category'],
                    'Quantity': quantity,
                    'Price': price,
                    'Total_Amount': round(total_amount, 2),
                    'Sales_Rep': row['Sales_Rep'],
                    'Month': month,
                    'Day_of_Week': day_of_week
                })
        
        print(f"Detailed report successfully written to '{detailed_output_filename}'")
        return True
        
    except Exception as e:
        print(f"Error creating detailed report: {e}")
        return False

def display_summary_file(filename):
    """
    Display the contents of the summary CSV file
    """
    try:
        print(f"\nContents of '{filename}':")
        print("=" * 80)
        
        with open(filename, 'r', newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            
            # Print header
            print(f"{'Type':<12} {'Name':<15} {'Total Sales':<12} {'Quantity':<10} {'Transactions':<12} {'Avg Sale':<10}")
            print("-" * 80)
            
            for row in csv_reader:
                print(f"{row['Type']:<12} {row['Name']:<15} ${float(row['Total_Sales']):<11.2f} "
                      f"{row['Total_Quantity']:<10} {row['Num_Transactions']:<12} ${float(row['Avg_Sale_Amount']):<9.2f}")
        
        print("-" * 80)
        
    except Exception as e:
        print(f"Error displaying summary file: {e}")

def main():
    input_file = "sales_data.csv"
    summary_file = "sales_summary.csv"
    detailed_file = "detailed_sales_report.csv"
    
    print("Processing sales data and creating reports...")
    print("=" * 50)
    
    # Create summary report
    if process_sales_and_create_summary(input_file, summary_file):
        display_summary_file(summary_file)
    
    # Create detailed report
    if create_detailed_report(input_file, detailed_file):
        print(f"\nBoth summary and detailed reports have been created successfully!")
        print(f"Summary report: {summary_file}")
        print(f"Detailed report: {detailed_file}")

if __name__ == "__main__":
    main()