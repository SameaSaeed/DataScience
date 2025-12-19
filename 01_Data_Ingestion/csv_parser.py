#!/usr/bin/env python3
"""
CSV Parser - A command-line tool for parsing and analyzing CSV files
"""

import csv
import argparse
import sys
from typing import List, Dict, Any, Optional

def read_csv_file(filename: str) -> List[Dict[str, Any]]:
    """
    Read CSV file and return list of dictionaries
    
    Args:
        filename (str): Path to the CSV file
        
    Returns:
        List[Dict[str, Any]]: List of rows as dictionaries
    """
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def is_numeric(value: str) -> bool:
    """
    Check if a string value can be converted to a number
    
    Args:
        value (str): String value to check
        
    Returns:
        bool: True if numeric, False otherwise
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

def convert_to_number(value: str) -> float:
    """
    Convert string to number (int or float)
    
    Args:
        value (str): String value to convert
        
    Returns:
        float: Converted number
    """
    try:
        # Try integer first
        if '.' not in value:
            return float(int(value))
        return float(value)
    except ValueError:
        return 0.0

def calculate_statistics(data: List[Dict[str, Any]], column: str) -> Dict[str, float]:
    """
    Calculate average, min, and max for a numerical column
    
    Args:
        data (List[Dict[str, Any]]): CSV data as list of dictionaries
        column (str): Column name to analyze
        
    Returns:
        Dict[str, float]: Dictionary with avg, min, max values
    """
    if not data:
        return {"avg": 0, "min": 0, "max": 0, "count": 0}
    
    # Check if column exists
    if column not in data[0]:
        print(f"Error: Column '{column}' not found in CSV file.")
        available_columns = list(data[0].keys())
        print(f"Available columns: {', '.join(available_columns)}")
        sys.exit(1)
    
    # Extract numerical values from the column
    numerical_values = []
    for row in data:
        value = row[column].strip()
        if is_numeric(value):
            numerical_values.append(convert_to_number(value))
        else:
            print(f"Warning: Non-numeric value '{value}' found in column '{column}', skipping...")

    if not numerical_values:
        print(f"Error: No numerical values found in column '{column}'")
        sys.exit(1)
    
    # Calculate statistics
    avg_value = sum(numerical_values) / len(numerical_values)
    min_value = min(numerical_values)
    max_value = max(numerical_values)
    
    return {
        "avg": round(avg_value, 2),
        "min": min_value,
        "max": max_value,
        "count": len(numerical_values)
    }

def display_statistics(stats: Dict[str, float], column: str) -> None:
    """
    Display statistics in a formatted way
    
    Args:
        stats (Dict[str, float]): Statistics dictionary
        column (str): Column name
    """
    print(f"\nStatistics for column '{column}':")
    print("-" * 40)
    print(f"Average: {stats['avg']}")
    print(f"Minimum: {stats['min']}")
    print(f"Maximum: {stats['max']}")
    print(f"Count: {stats['count']} values")

def filter_rows(data: List[Dict[str, Any]], filter_column: str, filter_value: str) -> List[Dict[str, Any]]:
    """
    Filter rows based on column value
    
    Args:
        data (List[Dict[str, Any]]): CSV data as list of dictionaries
        filter_column (str): Column to filter by
        filter_value (str): Value to filter for
        
    Returns:
        List[Dict[str, Any]]: Filtered data
    """
    if not data:
        return []
    
    # Check if filter column exists
    if filter_column not in data[0]:
        print(f"Error: Filter column '{filter_column}' not found in CSV file.")
        available_columns = list(data[0].keys())
        print(f"Available columns: {', '.join(available_columns)}")
        sys.exit(1)
    
    # Filter rows
    filtered_data = []
    for row in data:
        if row[filter_column].strip().lower() == filter_value.lower():
            filtered_data.append(row)
    
    return filtered_data

def display_filtered_data(data: List[Dict[str, Any]], filter_column: str, filter_value: str) -> None:
    """
    Display filtered data in a formatted table
    
    Args:
        data (List[Dict[str, Any]]): Filtered data
        filter_column (str): Column that was filtered
        filter_value (str): Value that was filtered for
    """
    if not data:
        print(f"No rows found where {filter_column} = '{filter_value}'")
        return
    
    print(f"\nRows where {filter_column} = '{filter_value}' ({len(data)} found):")
    print("-" * 60)
    
    # Get column headers
    headers = list(data[0].keys())
    
    # Print headers
    header_line = " | ".join(f"{header:15}" for header in headers)
    print(header_line)
    print("-" * len(header_line))
    
    # Print data rows
    for row in data:
        row_line = " | ".join(f"{str(row[header]):15}" for header in headers)
        print(row_line)

def create_argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure argument parser
    
    Returns:
        argparse.ArgumentParser: Configured parser
    """
    parser = argparse.ArgumentParser(
        description="CSV Parser - Analyze CSV files from command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=""" 
Examples:
  python csv_parser.py data.csv --column salary
  python csv_parser.py data.csv --column age --filter department Engineering
  python csv_parser.py data.csv --column salary --filter name "John Smith"
        """
    )
    
    parser.add_argument(
        'filename',
        help='Path to the CSV file to parse'
    )
    
    parser.add_argument(
        '--column', '-c',
        required=True,
        help='Column name to calculate statistics for (must contain numerical data)'
    )
    
    parser.add_argument(
        '--filter', '-f',
        nargs=2,
        metavar=('COLUMN', 'VALUE'),
        help='Filter rows by column value (format: --filter column_name value)'
    )
    
    parser.add_argument(
        '--show-data', '-s',
        action='store_true',
        help='Show filtered data in addition to statistics'
    )
    
    return parser

def main():
    """
    Main function to execute the CSV parser
    """
    # Parse command line arguments
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Read CSV file
    print(f"Reading CSV file: {args.filename}")
    data = read_csv_file(args.filename)
    
    if not data:
        print("Error: CSV file is empty or could not be read.")
        sys.exit(1)
    
    print(f"Successfully loaded {len(data)} rows of data.")
    
    # Apply filtering if specified
    if args.filter:
        filter_column, filter_value = args.filter
        print(f"Applying filter: {filter_column} = '{filter_value}'")
        filtered_data = filter_rows(data, filter_column, filter_value)
        
        if args.show_data:
            display_filtered_data(filtered_data, filter_column, filter_value)
        
        # Use filtered data for statistics
        data_for_stats = filtered_data
        
        if not data_for_stats:
            print("No data remaining after filtering. Cannot calculate statistics.")
            sys.exit(1)
    else:
        data_for_stats = data
    
    # Calculate and display statistics
    stats = calculate_statistics(data_for_stats, args.column)
    display_statistics(stats, args.column)
    
    # Show summary
    if args.filter:
        print(f"\nSummary: Analyzed {stats['count']} values from column '{args.column}' "
              f"where {args.filter[0]} = '{args.filter[1]}'")
    else:
        print(f"\nSummary: Analyzed {stats['count']} values from column '{args.column}' "
              f"across all {len(data)} rows")

if __name__ == "__main__":
    main()
