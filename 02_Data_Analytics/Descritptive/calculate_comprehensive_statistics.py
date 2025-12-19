#!/usr/bin/env python3
import csv
from collections import defaultdict

def calculate_sales_statistics(filename):
    """
    Calculate comprehensive statistics from sales data
    """
    sales_data = []
    
    # Read the CSV file
    try:
        with open(filename, 'r', newline='') as csvfile:
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
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
    # Calculate statistics
    if not sales_data:
        print("No data to process.")
        return None
    
    # Basic statistics
    total_sales = sum(record['total'] for record in sales_data)
    total_quantity = sum(record['quantity'] for record in sales_data)
    average_sale = total_sales / len(sales_data)
    
    # Sales by representative
    sales_by_rep = defaultdict(float)
    quantity_by_rep = defaultdict(int)
    
    # Sales by product
    sales_by_product = defaultdict(float)
    quantity_by_product = defaultdict(int)
    
    # Process data for detailed statistics
    for record in sales_data:
        rep = record['sales_rep']
        product = record['product']
        
        sales_by_rep[rep] += record['total']
        quantity_by_rep[rep] += record['quantity']
        
        sales_by_product[product] += record['total']
        quantity_by_product[product] += record['quantity']
    
    # Create statistics summary
    statistics = {
        'total_records': len(sales_data),
        'total_sales': total_sales,
        'total_quantity': total_quantity,
        'average_sale': average_sale,
        'sales_by_rep': dict(sales_by_rep),
        'quantity_by_rep': dict(quantity_by_rep),
        'sales_by_product': dict(sales_by_product),
        'quantity_by_product': dict(quantity_by_product)
    }
    
    # Display statistics
    print("SALES STATISTICS SUMMARY")
    print("=" * 50)
    print(f"Total Records: {statistics['total_records']}")
    print(f"Total Sales: ${statistics['total_sales']:,.2f}")
    print(f"Total Quantity Sold: {statistics['total_quantity']:,}")
    print(f"Average Sale Amount: ${statistics['average_sale']:.2f}")
    
    print("\nSALES BY REPRESENTATIVE:")
    print("-" * 30)
    for rep, sales in statistics['sales_by_rep'].items():
        quantity = statistics['quantity_by_rep'][rep]
        print(f"{rep}: ${sales:,.2f} ({quantity} items)")
    
    print("\nSALES BY PRODUCT:")
    print("-" * 30)
    for product, sales in statistics['sales_by_product'].items():
        quantity = statistics['quantity_by_product'][product]
        print(f"{product}: ${sales:,.2f} ({quantity} units)")
    
    return statistics

def main():
    filename = "sales_data.csv"
    statistics = calculate_sales_statistics(filename)

if __name__ == "__main__":
    main()