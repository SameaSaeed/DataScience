#!/usr/bin/env python3
"""
Weather Data Retrieval System
Automated weather data fetching using OpenWeatherMap API
"""

import requests
import json
from tabulate import tabulate
import sys
from datetime import datetime
import re

# API Configuration
API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def validate_city_name(city_name):
    """Validate city name input"""
    if not city_name or not city_name.strip():
        return False
    pattern = r'^[a-zA-Z\s\-]+$'
    return bool(re.match(pattern, city_name.strip()))

def get_weather_data(city_name):
    """Fetch weather data for a given city with error handling"""
    if not validate_city_name(city_name):
        print(f"Invalid city name: {city_name}")
        return None
    
    try:
        url = f"{BASE_URL}?q={city_name}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"City not found: {city_name}")
        elif response.status_code == 401:
            print("Invalid API key. Please check your API key.")
        else:
            print(f"API error for {city_name}: Status {response.status_code}")
        
        return None
        
    except requests.exceptions.Timeout:
        print(f"Timeout error for {city_name}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"Connection error for {city_name}")
        return None
    except Exception as e:
        print(f"Unexpected error for {city_name}: {e}")
        return None

def extract_weather_info(weather_data):
    """Extract relevant weather information from API response"""
    if not weather_data:
        return None
    
    try:
        extracted_info = {
            'City': weather_data['name'],
            'Country': weather_data['sys']['country'],
            'Temperature (°C)': weather_data['main']['temp'],
            'Feels Like (°C)': weather_data['main']['feels_like'],
            'Humidity (%)': weather_data['main']['humidity'],
            'Pressure (hPa)': weather_data['main']['pressure'],
            'Weather': weather_data['weather'][0]['description'].title(),
            'Wind Speed (m/s)': weather_data['wind']['speed'],
            'Visibility (m)': weather_data.get('visibility', 'N/A'),
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return extracted_info
        
    except KeyError as e:
        print(f"Error extracting data: Missing key {e}")
        return None

def display_weather_table(weather_data_list):
    """Display weather data in a formatted table"""
    if not weather_data_list:
        print("No weather data to display.")
        return
    
    headers = list(weather_data_list[0].keys())
    rows = [list(data.values()) for data in weather_data_list]
    
    print("\n" + "="*80)
    print("WEATHER DATA SUMMARY")
    print("="*80)
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print("="*80)

def display_weather_summary(weather_data_list):
    """Display summary statistics of weather data"""
    if not weather_data_list:
        return
    
    temperatures = [data['Temperature (°C)'] for data in weather_data_list]
    humidity_levels = [data['Humidity (%)'] for data in weather_data_list]
    
    summary_data = [
        ['Total Cities', len(weather_data_list)],
        ['Average Temperature (°C)', f"{sum(temperatures)/len(temperatures):.1f}"],
        ['Highest Temperature (°C)', f"{max(temperatures):.1f}"],
        ['Lowest Temperature (°C)', f"{min(temperatures):.1f}"],
        ['Average Humidity (%)', f"{sum(humidity_levels)/len(humidity_levels):.1f}"]
    ]
    
    print("\nWEATHER SUMMARY STATISTICS")
    print("-" * 40)
    print(tabulate(summary_data, headers=['Metric', 'Value'], tablefmt="simple"))

def main():
    """Main program function"""
    print("Weather Data Retrieval System")
    print("=" * 40)
    
    if API_KEY == "YOUR_API_KEY_HERE":
        print("Error: Please set your API key in the script!")
        print("Get your API key from: https://openweathermap.org/api")
        sys.exit(1)
    
    # Get cities from user input
    cities_input = input("Enter city names separated by commas: ").strip()
    
    if cities_input:
        cities = [city.strip() for city in cities_input.split(',')]
    else:
        cities = ['London', 'New York', 'Tokyo', 'Sydney', 'Paris']
        print(f"Using default cities: {', '.join(cities)}")
    
    # Fetch weather data
    weather_results = []
    for city in cities:
        print(f"Fetching weather data for {city}...")
        raw_data = get_weather_data(city)
        extracted_data = extract_weather_info(raw_data)
        
        if extracted_data:
            weather_results.append(extracted_data)
    
    # Display results
    if weather_results:
        display_weather_table(weather_results)
        display_weather_summary(weather_results)
    else:
        print("No weather data retrieved.")

if __name__ == "__main__":
    main()