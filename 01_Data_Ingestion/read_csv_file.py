#!/usr/bin/env python3
import csv
from datetime import datetime

def read_sales_data(filename):
    """
    Read sales data from CSV file using csv module
    """
    sales_data = []
    
    try:
        with open(filename, 'r', newline='') as csvfile:
            # Create CSV reader object
            csv_reader = csv.DictReader(csvfile)
            
            print("Sales Data:")
            print("-" * 80)
            print(f"{'Date':<12} {'Product':<12} {'Quantity':<8} {'Price':<8} {'Sales Rep':<15}")
            print("-" * 80)
            
            for row in csv_reader:
                # Process each row
                date = row['Date']
                product = row['Product']
                quantity = int(row['Quantity'])
                price = float(row['Price'])
                sales_rep = row['Sales_Rep']
                
                # Calculate total for this sale
                total = quantity * price
                
                # Store the data
                sale_record = {
                    'date': date,
                    'product': product,
                    'category': row['Category'],
                    'quantity': quantity,
                    'price': price,
                    'total': total,
                    'sales_rep': sales_rep
                }
                sales_data.append(sale_record)
                
                # Display the data
                print(f"{date:<12} {product:<12} {quantity:<8} ${price:<7.2f} {sales_rep:<15}")
            
            print("-" * 80)
            print(f"Total records processed: {len(sales_data)}")
            
        return sales_data
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

def main():
    filename = "sales_data.csv"
    sales_data = read_sales_data(filename)

if __name__ == "__main__":
    main()