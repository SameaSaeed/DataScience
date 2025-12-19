{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "db7b9b16",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "# Load the sample datasets\n",
    "hospital_data = pd.read_csv('hospital_data.csv')\n",
    "transport_data = pd.read_csv('transport_data.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5882e95a",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "hospital_data.info()\n",
    "hospital_data.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "057c29d5",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "def analyze_data_quality(df, dataset_name):\n",
    "\n",
    "    # Check for missing values\n",
    "    missing_values = df.isnull().sum()\n",
    "    \n",
    "    # Check for duplicates\n",
    "    print(f\"\\n2. Duplicate Rows: {df.duplicated().sum()}\")\n",
    "    \n",
    "    # Check data types\n",
    "    print(df.dtypes)\n",
    "    \n",
    "    # Check for potential outliers in numeric columns\n",
    "    numeric_cols = df.select_dtypes(include=[np.number]).columns\n",
    "    if len(numeric_cols) > 0:\n",
    "        print(df[numeric_cols].describe())\n",
    "\n",
    "# Analyze both datasets\n",
    "analyze_data_quality(hospital_data, \"Hospital\")\n",
    "analyze_data_quality(transport_data, \"Transport\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "59b38f8d",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "def clean_data(df, dataset_type=\"general\"):\n",
    "\n",
    "    # Create a copy to avoid modifying the original dataset\n",
    "    cleaned_df = df.copy()\n",
    "    \n",
    "    # Step 1: Handle missing values\n",
    "    cleaned_df = handle_missing_values(cleaned_df, dataset_type)\n",
    "    \n",
    "    # Step 2: Remove duplicates\n",
    "    cleaned_df = remove_duplicates(cleaned_df)\n",
    "    \n",
    "    # Step 3: Fix data types\n",
    "    cleaned_df = fix_data_types(cleaned_df, dataset_type)\n",
    "    \n",
    "    # Step 4: Handle outliers\n",
    "    cleaned_df = handle_outliers(cleaned_df, dataset_type)\n",
    "    \n",
    "    # Step 5: Standardize text data\n",
    "    cleaned_df = standardize_text_data(cleaned_df)\n",
    "    \n",
    "    print(f\"Cleaned dataset shape: {cleaned_df.shape}\")\n",
    "    print(\"Data cleaning completed successfully!\")\n",
    "    \n",
    "    return cleaned_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b86ca5d0",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "def handle_missing_values(df, dataset_type):\n",
    "\n",
    "    cleaned_df = df.copy()\n",
    "    \n",
    "    for column in cleaned_df.columns:\n",
    "        missing_count = cleaned_df[column].isnull().sum()\n",
    "        \n",
    "        if missing_count > 0:\n",
    "            print(f\"  - Processing {column}: {missing_count} missing values\")\n",
    "            \n",
    "            # Handle numeric columns\n",
    "            if cleaned_df[column].dtype in ['int64', 'float64']:\n",
    "\n",
    "                # Use median for numeric data\n",
    "                median_value = cleaned_df[column].median()\n",
    "                cleaned_df[column].fillna(median_value, inplace=True)\n",
    "                print(f\"    Filled with median: {median_value}\")\n",
    "            \n",
    "            # Handle categorical/text columns\n",
    "            elif cleaned_df[column].dtype == 'object':\n",
    "            \n",
    "                # Use mode (most frequent value) for categorical data\n",
    "                if not cleaned_df[column].mode().empty:\n",
    "                    mode_value = cleaned_df[column].mode()[0]\n",
    "                    cleaned_df[column].fillna(mode_value, inplace=True)\n",
    "                    print(f\"    Filled with mode: {mode_value}\")\n",
    "                else:\n",
    "                    # If no mode exists, use 'Unknown'\n",
    "                    cleaned_df[column].fillna('Unknown', inplace=True)\n",
    "                    print(f\"    Filled with: Unknown\")\n",
    "            \n",
    "            # Handle datetime columns\n",
    "            elif 'datetime' in str(cleaned_df[column].dtype):\n",
    "                # Forward fill for datetime data\n",
    "                cleaned_df[column].fillna(method='ffill', inplace=True)\n",
    "                print(f\"    Forward filled datetime values\")\n",
    "    \n",
    "    return cleaned_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "02e878b1",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "def remove_duplicates(df):\n",
    "\n",
    "    initial_count = len(df)\n",
    "    cleaned_df = df.drop_duplicates()\n",
    "    final_count = len(cleaned_df)\n",
    "    \n",
    "    duplicates_removed = initial_count - final_count\n",
    "    print(f\"  - Removed {duplicates_removed} duplicate rows\")\n",
    "    \n",
    "    return cleaned_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "19e852b1",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "def fix_data_types(df, dataset_type):  \n",
    "    cleaned_df = df.copy()\n",
    "    \n",
    "    # Common data type fixes\n",
    "    for column in cleaned_df.columns:\n",
    "        \n",
    "        # Convert string numbers to numeric\n",
    "        if cleaned_df[column].dtype == 'object':\n",
    "            # Try to convert to numeric if it looks like numbers\n",
    "            try:\n",
    "                # Check if all non-null values can be converted to numbers\n",
    "                pd.to_numeric(cleaned_df[column].dropna(), errors='raise')\n",
    "                cleaned_df[column] = pd.to_numeric(cleaned_df[column], errors='coerce')\n",
    "                print(f\"  - Converted {column} to numeric\")\n",
    "            except:\n",
    "                pass\n",
    "        \n",
    "        # Dataset-specific type conversions\n",
    "        if dataset_type == \"hospital\":\n",
    "            # Hospital-specific conversions\n",
    "            if 'date' in column.lower() or 'time' in column.lower():\n",
    "                try:\n",
    "                    cleaned_df[column] = pd.to_datetime(cleaned_df[column])\n",
    "                    print(f\"  - Converted {column} to datetime\")\n",
    "                except:\n",
    "                    pass\n",
    "            \n",
    "            if 'id' in column.lower():\n",
    "                cleaned_df[column] = cleaned_df[column].astype(str)\n",
    "                print(f\"  - Converted {column} to string\")\n",
    "        \n",
    "        elif dataset_type == \"transport\":\n",
    "            # Transport-specific conversions\n",
    "            if 'date' in column.lower() or 'time' in column.lower():\n",
    "                try:\n",
    "                    cleaned_df[column] = pd.to_datetime(cleaned_df[column])\n",
    "                    print(f\"  - Converted {column} to datetime\")\n",
    "                except:\n",
    "                    pass\n",
    "    \n",
    "    return cleaned_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3f9f19d8",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "def handle_outliers(df, dataset_type):\n",
    "    cleaned_df = df.copy()\n",
    "    numeric_columns = cleaned_df.select_dtypes(include=[np.number]).columns\n",
    "    \n",
    "    for column in numeric_columns:\n",
    "        # Calculate IQR\n",
    "        Q1 = cleaned_df[column].quantile(0.25)\n",
    "        Q3 = cleaned_df[column].quantile(0.75)\n",
    "        IQR = Q3 - Q1\n",
    "        \n",
    "        # Define outlier bounds\n",
    "        lower_bound = Q1 - 1.5 * IQR\n",
    "        upper_bound = Q3 + 1.5 * IQR\n",
    "        \n",
    "        # Count outliers\n",
    "        outliers = cleaned_df[(cleaned_df[column] < lower_bound) | \n",
    "                             (cleaned_df[column] > upper_bound)]\n",
    "        \n",
    "        if len(outliers) > 0:\n",
    "            print(f\"  - Found {len(outliers)} outliers in {column}\")\n",
    "            \n",
    "            # Cap outliers instead of removing them\n",
    "            cleaned_df[column] = cleaned_df[column].clip(lower=lower_bound, \n",
    "                                                        upper=upper_bound)\n",
    "            print(f\"    Capped outliers to range [{lower_bound:.2f}, {upper_bound:.2f}]\")\n",
    "    \n",
    "    return cleaned_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d7cfa468",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "def standardize_text_data(df):\n",
    "    cleaned_df = df.copy()\n",
    "    text_columns = cleaned_df.select_dtypes(include=['object']).columns\n",
    "    \n",
    "    for column in text_columns:\n",
    "        if cleaned_df[column].dtype == 'object':\n",
    "            # Remove leading/trailing whitespace\n",
    "            cleaned_df[column] = cleaned_df[column].astype(str).str.strip()\n",
    "            \n",
    "            # Convert to title case for names and categories\n",
    "            if any(keyword in column.lower() for keyword in ['name', 'category', 'type', 'status']):\n",
    "                cleaned_df[column] = cleaned_df[column].str.title()\n",
    "                print(f\"  - Standardized {column} to title case\")\n",
    "            \n",
    "            # Convert to uppercase for codes and IDs\n",
    "            elif any(keyword in column.lower() for keyword in ['code', 'id']):\n",
    "                cleaned_df[column] = cleaned_df[column].str.upper()\n",
    "                print(f\"  - Standardized {column} to uppercase\")\n",
    "            \n",
    "            # Remove extra spaces\n",
    "            cleaned_df[column] = cleaned_df[column].str.replace(r'\\s+', ' ', regex=True)\n",
    "    \n",
    "    return cleaned_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "993626b2",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "# Apply cleaning pipeline\n",
    "hospital_cleaned = clean_data(hospital_data, dataset_type=\"hospital\")\n",
    "transport_cleaned = clean_data(transport_data, dataset_type=\"transport\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "dbdb4d22",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "def validate_cleaning_results(original_df, cleaned_df, dataset_name):\n",
    "\n",
    "    # Check 1: No missing values in critical columns\n",
    "    missing_after = cleaned_df.isnull().sum().sum()\n",
    "    print(f\"✓ Total missing values after cleaning: {missing_after}\")\n",
    "    \n",
    "    # Check 2: No duplicates\n",
    "    duplicates_after = cleaned_df.duplicated().sum()\n",
    "    print(f\"✓ Duplicate rows after cleaning: {duplicates_after}\")\n",
    "    \n",
    "    # Check 3: Data types are appropriate\n",
    "    print(\"✓ Data types after cleaning:\")\n",
    "    for col, dtype in cleaned_df.dtypes.items():\n",
    "        print(f\"  - {col}: {dtype}\")\n",
    "    \n",
    "    # Check 4: Data integrity maintained\n",
    "    rows_removed = len(original_df) - len(cleaned_df)\n",
    "    print(f\"✓ Rows removed during cleaning: {rows_removed}\")\n",
    "    \n",
    "    # Check 5: Basic statistics\n",
    "    numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns\n",
    "    if len(numeric_cols) > 0:\n",
    "        print(\"✓ Numeric data ranges are reasonable:\")\n",
    "        for col in numeric_cols:\n",
    "            min_val = cleaned_df[col].min()\n",
    "            max_val = cleaned_df[col].max()\n",
    "            print(f\"  - {col}: [{min_val:.2f}, {max_val:.2f}]\")\n",
    "    \n",
    "    print(f\"✓ {dataset_name} dataset cleaning validation completed!\")\n",
    "\n",
    "# Validate both datasets\n",
    "validate_cleaning_results(hospital_original, hospital_cleaned, \"Hospital\")\n",
    "validate_cleaning_results(transport_original, transport_cleaned, \"Transport\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1f588895",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "def complete_data_cleaning_pipeline(df, dataset_type=\"general\", save_results=False):\n",
    "\n",
    "    # Store original data\n",
    "    original_df = df.copy()\n",
    "    \n",
    "    # Apply cleaning pipeline\n",
    "    cleaned_df = clean_data(df, dataset_type)\n",
    "    \n",
    "    # Generate cleaning report\n",
    "    cleaning_report = generate_cleaning_report(original_df, cleaned_df, dataset_type)\n",
    "    \n",
    "    # Save results if requested\n",
    "    if save_results:\n",
    "        filename = f\"{dataset_type}_cleaned_data.csv\"\n",
    "        cleaned_df.to_csv(filename, index=False)\n",
    "        print(f\"✓ Cleaned data saved to {filename}\")\n",
    "    \n",
    "    # Return results\n",
    "    results = {\n",
    "        'original_data': original_df,\n",
    "        'cleaned_data': cleaned_df,\n",
    "        'cleaning_report': cleaning_report\n",
    "    }\n",
    "    \n",
    "    return results\n",
    "\n",
    "def generate_cleaning_report(original_df, cleaned_df, dataset_type):\n",
    "    \"\"\"\n",
    "    Generate a comprehensive cleaning report\n",
    "    \"\"\"\n",
    "    report = {\n",
    "        'dataset_type': dataset_type,\n",
    "        'original_shape': original_df.shape,\n",
    "        'cleaned_shape': cleaned_df.shape,\n",
    "        'rows_removed': len(original_df) - len(cleaned_df),\n",
    "        'missing_values_before': original_df.isnull().sum().sum(),\n",
    "        'missing_values_after': cleaned_df.isnull().sum().sum(),\n",
    "        'duplicates_before': original_df.duplicated().sum(),\n",
    "        'duplicates_after': cleaned_df.duplicated().sum(),\n",
    "        'data_types_changed': []\n",
    "    }\n",
    "    \n",
    "    # Check for data type changes\n",
    "    for col in original_df.columns:\n",
    "        if col in cleaned_df.columns:\n",
    "            if original_df[col].dtype != cleaned_df[col].dtype:\n",
    "                report['data_types_changed'].append({\n",
    "                    'column': col,\n",
    "                    'from': str(original_df[col].dtype),\n",
    "                    'to': str(cleaned_df[col].dtype)\n",
    "                })\n",
    "    \n",
    "    return report"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a5d31ad3",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "# Apply complete pipeline to hospital data\n",
    "hospital_results = complete_data_cleaning_pipeline(\n",
    "    hospital_data, \n",
    "    dataset_type=\"hospital\", \n",
    "    save_results=True\n",
    ")\n",
    "\n",
    "# Apply complete pipeline to transport data\n",
    "transport_results = complete_data_cleaning_pipeline(\n",
    "    transport_data, \n",
    "    dataset_type=\"transport\", \n",
    "    save_results=True\n",
    ")\n",
    "\n",
    "# Display cleaning reports\n",
    "def display_cleaning_report(results, dataset_name):\n",
    "    \"\"\"\n",
    "    Display a formatted cleaning report\n",
    "    \"\"\"\n",
    "    report = results['cleaning_report']\n",
    "    \n",
    "    print(f\"\\n{'='*50}\")\n",
    "    print(f\"CLEANING REPORT: {dataset_name.upper()}\")\n",
    "    print(f\"{'='*50}\")\n",
    "    print(f\"Dataset Type: {report['dataset_type']}\")\n",
    "    print(f\"Original Shape: {report['original_shape']}\")\n",
    "    print(f\"Cleaned Shape: {report['cleaned_shape']}\")\n",
    "    print(f\"Rows Removed: {report['rows_removed']}\")\n",
    "    print(f\"Missing Values Before: {report['missing_values_before']}\")\n",
    "    print(f\"Missing Values After: {report['missing_values_after']}\")\n",
    "    print(f\"Duplicates Before: {report['duplicates_before']}\")\n",
    "    print(f\"Duplicates After: {report['duplicates_after']}\")\n",
    "    \n",
    "    if report['data_types_changed']:\n",
    "        print(\"\\nData Type Changes:\")\n",
    "        for change in report['data_types_changed']:\n",
    "            print(f\"  - {change['column']}: {change['from']} → {change['to']}\")\n",
    "    else:\n",
    "        print(\"\\nNo data type changes made\")\n",
    "\n",
    "# Display reports for both datasets\n",
    "display_cleaning_report(hospital_results, \"Hospital\")\n",
    "display_cleaning_report(transport_results, \"Transport\")"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
