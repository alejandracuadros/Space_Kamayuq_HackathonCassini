import os
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
from scipy.stats import zscore

# Function to parse an XML file and extract all data dynamically
def parse_cdm_file_all(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    data = {"FileName": os.path.basename(file_path)}

    # Helper function to parse an XML section recursively
    def parse_section(section, prefix=""):
        if section is None:
            return {}
        parsed_data = {}
        for elem in section:
            tag = prefix + elem.tag.split("}")[-1]  # Remove namespace if present
            if list(elem):  # If the element has children
                parsed_data.update(parse_section(elem, prefix=f"{tag}_"))
            else:
                parsed_data[tag] = elem.text.strip() if elem.text else None
        return parsed_data

    # Extract all major sections
    data.update(parse_section(root.find(".//header"), prefix="Header_"))
    data.update(parse_section(root.find(".//relativeMetadataData"), prefix="Metadata_"))
    data.update(parse_section(root.find(".//segment/metadata[OBJECT='OBJECT1']"), prefix="Object1_"))
    data.update(parse_section(root.find(".//segment/metadata[OBJECT='OBJECT2']"), prefix="Object2_"))
    data.update(parse_section(root.find(".//covarianceMatrix"), prefix="Covariance_"))

    return data

# File paths for the CSPOC XML files
file_paths = [
    "cdms/CSPOC_0.xml",
    "cdms/CSPOC_1.xml",
    "cdms/CSPOC_2.xml",
    "cdms/CSPOC_8.xml",
    "cdms/CSPOC_9.xml",
    "cdms/CSPOC_10.xml",
    "cdms/CSPOC_11.xml",
    "cdms/CSPOC_12.xml",
    "cdms/CSPOC_13.xml",
    "cdms/CSPOC_14.xml",
]

# Parse all files and collect data dynamically
parsed_data = [parse_cdm_file_all(file_path) for file_path in file_paths]

# Convert to DataFrame for better organization and analysis
df = pd.DataFrame(parsed_data)

# Save the DataFrame as a CSV file for review or further processing
output_file = "cspoc_extracted_data.csv"
df.to_csv(output_file, index=False)
print(f"Data successfully saved to {output_file}")

"""

Analyzing the data

"""
# Load the uploaded CSV file for analysis
file_path = "cspoc_extracted_data.csv"
df = pd.read_csv(file_path)

# Data Cleaning: Convert numeric fields
for col in ['Metadata_MISS_DISTANCE', 'Metadata_RELATIVE_SPEED', 'Header_CREATION_DATE', 'Metadata_TCA']:
    if 'DISTANCE' in col or 'SPEED' in col:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Parse datetime fields
df['Header_CREATION_DATE'] = pd.to_datetime(df['Header_CREATION_DATE'], errors='coerce')
df['Metadata_TCA'] = pd.to_datetime(df['Metadata_TCA'], errors='coerce')

# 1. Statistics and Comparison
# Calculate key statistics
stats = df.describe()

# Identify potential outliers using z-scores (standard deviations from the mean)
df['MissDistance_z'] = zscore(df['Metadata_MISS_DISTANCE'], nan_policy='omit')
df['RelativeSpeed_z'] = zscore(df['Metadata_RELATIVE_SPEED'], nan_policy='omit')

# Reliability Metric:
# Define reliability as a combination of:
# - Smaller Miss Distance
# - Smaller Relative Speed
# - Earlier Creation Date

# Normalize key metrics for comparability
df['Norm_MissDistance'] = (df['Metadata_MISS_DISTANCE'] - df['Metadata_MISS_DISTANCE'].min()) / (
    df['Metadata_MISS_DISTANCE'].max() - df['Metadata_MISS_DISTANCE'].min())
df['Norm_RelativeSpeed'] = (df['Metadata_RELATIVE_SPEED'] - df['Metadata_RELATIVE_SPEED'].min()) / (
    df['Metadata_RELATIVE_SPEED'].max() - df['Metadata_RELATIVE_SPEED'].min())
df['Norm_CreationDate'] = (df['Header_CREATION_DATE'] - df['Header_CREATION_DATE'].min()) / (
    df['Header_CREATION_DATE'].max() - df['Header_CREATION_DATE'].min())

# Weighted reliability score (lower is better)
df['Reliability_Score'] = (
    df['Norm_MissDistance'] * 0.4 +
    df['Norm_RelativeSpeed'] * 0.4 +
    df['Norm_CreationDate'] * 0.2
)

# Best (most reliable) file
most_reliable = df.loc[df['Reliability_Score'].idxmin()]

# 2. Correlation Analysis
correlation = df[['Metadata_MISS_DISTANCE', 'Metadata_RELATIVE_SPEED']].corr()

# 3. Aggregated Statistics
grouped_stats = df.groupby('Object1_OBJECT_NAME').agg({
    'Metadata_MISS_DISTANCE': ['mean', 'std', 'min', 'max'],
    'Metadata_RELATIVE_SPEED': ['mean', 'std', 'min', 'max']
}).reset_index()

# Save results as CSV files for further review
stats.to_csv("key_statistics_cspoc.csv", index=True)
correlation.to_csv("correlation_analysis_cspoc.csv", index=True)
grouped_stats.to_csv("grouped_statistics_cspoc.csv", index=False)

# Display the key findings directly in the console
print("\n--- CSPOC Key Statistics ---")
print(stats)

print("\n--- CSPOC Correlation Analysis ---")
print(correlation)

print("\n--- CSPOC Grouped Statistics by Object ---")
print(grouped_stats)

print("\n--- Most Reliable Entry ---")
print(most_reliable)

# Save the most reliable entry as a separate CSV file
most_reliable.to_csv("most_reliable_entry_cspoc.csv", header=True)
